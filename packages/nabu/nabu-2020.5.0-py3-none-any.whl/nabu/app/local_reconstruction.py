from os.path import join, isfile, basename, dirname
from math import ceil
import gc
from psutil import virtual_memory
from silx.io import get_data
from silx.io.url import DataUrl
from ..resources.logger import LoggerOrPrint
from ..io.writer import merge_hdf5_files, NXProcessWriter
from ..cuda.utils import collect_cuda_gpus
from ..resources.computations import estimate_chunk_size
from ..preproc.phase import compute_paganin_margin
from ..app.fullfield_cuda import CudaFullFieldPipeline, CudaFullFieldPipelineLimitedMemory
from ..misc.histogram import PartialHistogram, add_last_bin, hist_as_2Darray

def get_gpus_ids(resources_cfg):
    gpus_ids = resources_cfg["gpu_id"]
    if gpus_ids != []:
        return gpus_ids
    # TODO (?) heuristic to pick the best gpus
    return list(range(resources_cfg["gpus"]))



class LocalReconstruction:

    _pipeline_cls = CudaFullFieldPipeline

    def __init__(self, process_config, logger=None, extra_options=None, cuda_options=None):
        self.process_config = process_config
        self.logger = LoggerOrPrint(logger)
        self._set_extra_options(extra_options)
        self._get_reconstruction_range()
        self._get_resources()
        self._compute_max_chunk_size()
        self._compute_phase_margin()
        self._get_pipeline_class()
        self._compute_volume_chunks()
        self.pipeline = None
        self.cuda_options = cuda_options


    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {
            "gpu_mem_fraction": 0.9,
            "cpu_mem_fraction": 0.9,
            "use_phase_margin": True,
            "max_chunk_size": None,
            "phase_margin": None,
        }
        advanced_options.update(extra_options)
        self.extra_options = advanced_options
        self.gpu_mem_fraction = self.extra_options["gpu_mem_fraction"]
        self.cpu_mem_fraction = self.extra_options["cpu_mem_fraction"]
        self.use_phase_margin = self.extra_options["use_phase_margin"]
        self._do_histograms = self.process_config.nabu_config["postproc"]["output_histogram"]
        self._histogram_merged = False


    def _get_reconstruction_range(self):
        rec_cfg = self.process_config.nabu_config["reconstruction"]
        self.z_min = rec_cfg["start_z"]
        self.z_max = rec_cfg["end_z"] + 1
        self.delta_z = self.z_max - self.z_min


    def _get_resources(self):
        self.resources = {}
        self._get_gpu()
        self._get_memory()


    def _get_memory(self):
        vm = virtual_memory()
        self.resources["mem_avail_GB"] = vm.available / 1e9


    def _get_gpu(self):
        gpus = get_gpus_ids(self.process_config.nabu_config["resources"])
        if len(gpus) == 0:
            raise ValueError("Need at least one GPU")
        if len(gpus) > 1:
            raise ValueError("This class does not support more than one GPU")
        self.resources["gpu_id"] = self._gpu_id = gpus[0]
        self.resources["gpus"] = collect_cuda_gpus()


    def _compute_max_chunk_size(self):
        gpu_mem = self.resources["gpus"][self._gpu_id]["memory_GB"] * self.gpu_mem_fraction
        cpu_mem = self.resources["mem_avail_GB"] * self.cpu_mem_fraction
        self.gpu_max_chunk_size = estimate_chunk_size(
            gpu_mem,
            self.process_config,
            chunk_step=10
        )
        self.cpu_max_chunk_size = estimate_chunk_size(
            cpu_mem,
            self.process_config,
            chunk_step=10
        )
        user_max_chunk_size = self.extra_options["max_chunk_size"]
        if user_max_chunk_size is not None:
            self.gpu_max_chunk_size = min(self.gpu_max_chunk_size, user_max_chunk_size)
            self.cpu_max_chunk_size = min(self.cpu_max_chunk_size, user_max_chunk_size)


    def _compute_phase_margin(self):
        unsharp_margin = self._compute_unsharp_margin()
        if "phase" not in self.process_config.processing_steps:
            self._phase_margin = unsharp_margin
            self._margin_v = self._phase_margin[0]
            return
        radio_shape = self.process_config.dataset_infos.radio_dims[::-1]
        opts = self.process_config.processing_options["phase"]
        user_phase_margin = self.extra_options["phase_margin"]
        if user_phase_margin is not None and user_phase_margin > 0:
            margin_v, margin_h = user_phase_margin, user_phase_margin
        else:
            margin_v, margin_h = compute_paganin_margin(
                radio_shape,
                distance=opts["distance_cm"],
                energy=opts["energy_kev"],
                delta_beta=opts["delta_beta"],
                pixel_size=opts["pixel_size_microns"],
                padding=opts["padding_type"]
            )
        margin_v = max(margin_v, unsharp_margin[0])
        self._phase_margin = (margin_v, margin_h)
        self._margin_v = self._phase_margin[0]
        self.logger.info("Estimated phase margin: %d pixels" % self._margin_v)


    def _compute_unsharp_margin(self):
        if "unsharp_mask" not in self.process_config.processing_steps:
            return (0, 0)
        opts = self.process_config.processing_options["unsharp_mask"]
        sigma = opts["unsharp_sigma"]
        # nabu uses cutoff = 4
        cutoff = 4
        gaussian_kernel_size = int(ceil(2 * cutoff * sigma + 1))
        self.logger.debug("Unsharp mask margin: %d pixels" % gaussian_kernel_size)
        return (gaussian_kernel_size, gaussian_kernel_size)


    def _get_pipeline_class(self):
        self._limited_mem = False
        # Actually less in some cases (margin_far_up + margin_far_down instead of 2*margin_v).
        # But we want to use only one class for all stages.
        chunk_size_for_one_slice = 1 + 2 * self._margin_v
        chunk_is_too_small = False
        if chunk_size_for_one_slice > self.gpu_max_chunk_size:
            msg = str(
                "Phase margin is %d, so we need to process at least %d detector rows. However, the available memory enables to process only %d rows at once"
                % (self._margin_v, chunk_size_for_one_slice, self.gpu_max_chunk_size)
            )
            chunk_is_too_small = True
        if self._margin_v > self.gpu_max_chunk_size//3:
            n_slices = max(1, self.gpu_max_chunk_size - (2 * self._margin_v))
            n_stages = ceil(self.delta_z / n_slices)
            if n_stages > 1:
                # In this case, using CudaFlatField + margin would lead to many stages
                msg = str(
                    "Phase margin (%d) is too big for chunk size (%d)"
                    % (self._margin_v, self.gpu_max_chunk_size)
                )
                chunk_is_too_small = True
        if chunk_is_too_small:
            self.logger.warning(msg)
            if self.use_phase_margin:
                self._pipeline_cls = CudaFullFieldPipelineLimitedMemory
                self.logger.warning("Using CudaFullFieldPipelineLimitedMemory")
                self._limited_mem = True
            else:
                self._phase_margin = (0, 0)
                self._margin_v = self._phase_margin[0]
                self._pipeline_cls = CudaFullFieldPipeline
                self.logger.warning("Using CudaFullFieldPipeline without margin")


    def _compute_volume_chunks(self):
        n_z = self.process_config.dataset_infos._radio_dims_notbinned[1]
        margin_v = self._margin_v
        self._margin_far_up = min(margin_v, self.z_min)
        self._margin_far_down = min(margin_v, n_z - (self.z_max + 1))
        # | margin_up |     n_slices    |  margin_down |
        # |-----------|-----------------|--------------|
        # |----------------------------------------------------|
        #                    delta_z
        if self._limited_mem:
            n_slices = self.cpu_max_chunk_size
        else:
            n_slices = self.gpu_max_chunk_size - (2 * margin_v)
        tasks = []
        if n_slices >= self.delta_z:
            # In this case we can do everything in a single stage
            n_slices = self.delta_z
            (margin_up, margin_down) = (self._margin_far_up, self._margin_far_down)
            tasks.append({
                "sub_region": (self.z_min - margin_up, self.z_max + margin_down),
                "phase_margin": ((margin_up, margin_down), (0, 0))
            })
        if self.gpu_max_chunk_size >= self.delta_z and self.z_min == 0 and self.z_max == n_z:
            # In this case we can do everything in a single stage, without margin
            n_slices = self.delta_z
            tasks.append({
                "sub_region": (self.z_min, self.z_max),
                "phase_margin": None,
            })
        else:
            # In this case there are at least two stages
            n_stages = ceil(self.delta_z / n_slices)
            tasks = []
            curr_z_min = self.z_min
            curr_z_max = self.z_min + n_slices
            for i in range(n_stages):
                margin_up = min(margin_v, curr_z_min)
                margin_down = min(margin_v, max(n_z - curr_z_max, 0))
                if curr_z_max + margin_down >= self.z_max:
                    curr_z_max -= (curr_z_max - (self.z_max + 0))
                    margin_down = min(margin_v, max(n_z - 1 - curr_z_max, 0))
                tasks.append({
                    "sub_region": (curr_z_min - margin_up, curr_z_max + margin_down),
                    "phase_margin": ((margin_up, margin_down), (0, 0))
                })
                if curr_z_max == self.z_max:
                    # No need for further tasks
                    break
                curr_z_min += n_slices
                curr_z_max += n_slices
        self.tasks = tasks
        self.n_slices = n_slices


    def _print_tasks(self):
        for task in self.tasks:
            margin_up, margin_down = task["phase_margin"][0]
            s_u, s_d = task["sub_region"]
            print(
                "Top Margin: [%04d, %04d[  |  Slices: [%04d, %04d[  |  Bottom Margin: [%04d, %04d["
                % (
                    s_u, s_u + margin_up,
                    s_u + margin_up, s_d - margin_down,
                    s_d - margin_down, s_d
                )
            )


    def _instantiate_pipeline(self, task):
        self.logger.debug("Creating a new pipeline object")
        args = [self.process_config, task["sub_region"]]
        if self._limited_mem:
            # Adapt chunk size so that [margin_up, chunk_size, margin_down]
            # is equal to delta_z.
            chunk_size = self.gpu_max_chunk_size
            dz = self._get_delta_z(task)
            margin_v_tot = sum(task["phase_margin"][0])
            args.append(chunk_size)
        pipeline = self._pipeline_cls(
            *args,
            logger=self.logger,
            phase_margin=task["phase_margin"],
            cuda_options=self.cuda_options
        )
        self.pipeline = pipeline


    def _instantiate_pipeline_if_necessary(self, current_task, other_task):
        """
        Instantiate a pipeline only if current_task has a different "delta z" than other_task
        """
        if self.pipeline is None:
            self._instantiate_pipeline(current_task)
            return
        dz_cur = self._get_delta_z(current_task)
        dz_other = self._get_delta_z(other_task)
        if dz_cur != dz_other:
            self.logger.debug("Destroying pipeline instance and releasing memory")
            self.pipeline = None
            # Not elegant, but for now the only way to release Cuda memory
            gc.collect()
            self._instantiate_pipeline(current_task)


    @staticmethod
    def _get_delta_z(task):
        # will have to be modified if sub_region accounts for x-subregion
        return task["sub_region"][1] - task["sub_region"][0]


    def reconstruct(self):
        tasks = self.tasks
        self.results = {}
        self._histograms = {}
        prev_task = tasks[0]
        for task in tasks:
            self.logger.info("\nProcessing sub-volume %s" % (str(task["sub_region"])))
            self._instantiate_pipeline_if_necessary(task, prev_task)
            self.pipeline.process_chunk(sub_region=task["sub_region"])
            task_key = self.pipeline.sub_region[-2:]
            self.results[task_key] = self.pipeline.writer.fname
            if self.pipeline.histogram_writer is not None: # self._do_histograms
                self._histograms[task_key] = self.pipeline.histogram_writer.fname
            prev_task = task


    def get_relative_files(self, files=None):
        out_cfg = self.process_config.nabu_config["output"]
        if files is None:
            files = list(self.results.values())
        files.sort()
        local_files = [
            join(out_cfg["file_prefix"], basename(fname))
            for fname in files
        ]
        return local_files


    def merge_hdf5_reconstructions(self, output_file=None):
        """
        Merge existing reconstructions by creating a HDF5 virtual dataset.

        Parameters
        ----------
        output_file: str, optional
            Output file name. If not given, the file prefix in section "output"
            of nabu config will be taken.
        """
        out_cfg = self.process_config.nabu_config["output"]
        out_dir = out_cfg["location"]
        # prevent issue when out_dir is empty, which happens only if dataset/location is a relative path.
        # this should be prevented earlier
        if out_dir is None or len(out_dir.strip()) == 0:
            out_dir = dirname(dirname(self.results[list(self.results.keys())[0]]))
        #
        if output_file is None:
            output_file = join(out_dir, out_cfg["file_prefix"]) + ".hdf5"
        if isfile(output_file):
            msg = str("File %s already exists" % output_file)
            if out_cfg["overwrite_results"]:
                msg += ". Overwriting as requested in configuration file"
                self.logger.warning(msg)
            else:
                msg += ". Set overwrite_results to True in [output] to overwrite existing files."
                self.logger.fatal(msg)
                raise ValueError(msg)
        local_files = self.get_relative_files()
        if local_files == []:
            self.logger.error("No files to merge")
            return
        entry = getattr(self.process_config.dataset_infos.dataset_scanner, "entry", "entry")
        # TODO "reconstruction" is hard-coded, might be problematic in the future
        h5_path = join(entry, *["reconstruction", "results", "data"])
        process_name = "reconstruction"
        #
        self.logger.info("Merging reconstructions to %s" % output_file)
        merge_hdf5_files(
            local_files, h5_path, output_file, process_name,
            output_entry=entry,
            output_filemode="a",
            processing_index=0,
            config={
                "reconstruction_stages": {
                    str(k): v for k, v in zip(self.results.keys(), local_files)
                },
                "nabu_config": self.process_config.nabu_config,
                "processing_options": self.process_config.processing_options,
            },
            base_dir=out_dir,
            overwrite=out_cfg["overwrite_results"]
        )
        self.merge_histograms(output_file=output_file)


    def merge_histograms(self, output_file=None, force_merge=False):
        """
        Merge the partial histograms
        """
        if not(self._do_histograms):
            return
        if self._histogram_merged and not(force_merge):
            return
        self.logger.info("Merging histograms")

        masterfile_entry = getattr(self.process_config.dataset_infos.dataset_scanner, "entry", "entry")
        masterfile_process_name = "histogram" # TODO don't hardcode process name
        output_entry = masterfile_entry

        out_cfg = self.process_config.nabu_config["output"]
        if output_file is None:
            output_file = join(
                dirname(list(self._histograms.values())[0]),
                out_cfg["file_prefix"] + "_histogram"
            ) + ".hdf5"
        local_files = self.get_relative_files(list(self._histograms.values()))
        #
        h5_path = join(masterfile_entry, *[masterfile_process_name, "results", "data"])
        #
        files = sorted(self._histograms.values())
        data_urls = []
        for fname in files:
            url = DataUrl(
                file_path=fname, data_path=h5_path, data_slice=None, scheme="silx"
            )
            data_urls.append(url)
        histograms = []
        for data_url in data_urls:
            h2D = get_data(data_url)
            histograms.append(
                (h2D[0], add_last_bin(h2D[1]))
            )
        histograms_merger = PartialHistogram( # TODO configurable
            method="fixed_bins_number", num_bins=histograms[0][0].size
        )
        merged_hist = histograms_merger.merge_histograms(histograms)

        writer = NXProcessWriter(
            output_file, entry=output_entry, filemode="a", overwrite=True
        )
        writer.write(
            hist_as_2Darray(merged_hist),
            "histogram", # TODO don't hard-code
            processing_index=1,
            config={
                "files": local_files,
                "bins": self.process_config.nabu_config["postproc"]["histogram_bins"],
                "volume_shape": (self.delta_z, ) + self.process_config.dataset_infos.radio_dims[::-1],
            }
        )
        self._histogram_merged = True

