import os
from ..utils import PlaceHolder, DataPlaceHolder, copy_dict_items
from ..io.config import NabuConfigParser, validate_nabu_config
from .utils import is_hdf5_extension
from .dataset_analyzer import analyze_dataset, DatasetAnalyzer
from .dataset_validator import NabuValidator
from .cor import CORFinder
from .logger import Logger, PrinterLogger


class ProcessConfig:
    """
    A class for describing the Nabu process configuration.
    """

    def __init__(
        self,
        conf_fname=None,
        conf_dict=None,
        dataset_infos=None,
        checks=True,
        remove_unused_radios=True,
        create_logger=False,
    ):
        """
        Initialize a ProcessConfig class.

        Parameters
        ----------
        conf_fname: str
            Path to the nabu configuration file. If provided, the parameters
            `conf_dict` and `dataset_infos` are ignored.
        conf_dict: dict
            A dictionary describing the nabu processing steps.
            If provided, it should be provided along with `dataset_infos` ; in this
            case, the parameter `conf_fname` is ignored.
        dataset_infos: DatasetAnalyzer
            A `DatasetAnalyzer` class instance.
            If provided, it should be provided along with `conf_dict` ; in this
            case, the parameter `conf_fname` is ignored.
        checks: bool, optional, default is True
            Whether to perform checks on configuration and datasets (recommended !)
        remove_unused_radios: bool, optional, default is True
            Whether to remove unused radios, i.e radios present in the dataset,
            but not explicitly listed in the scan metadata.
        create_logger: str or bool, optional
            Whether to create a Logger object. Default is False, meaning that the logger
            object creation is left to the user.
            If set to True, a Logger object is created, and logs will be written
            to the file "nabu_dataset_name.log".
            If set to a string, a Logger object is created, and the logs will be written
            to the file specified by this string.
        """
        args_error_msg = (
            "You must either provide conf_fname, or (conf_dict and dataset_infos)"
        )
        self.conf_fname = conf_fname
        if conf_fname is not None:
            if (conf_dict is not None) or (dataset_infos is not None):
                raise ValueError(args_error_msg)
            if not (os.path.isfile(conf_fname)):
                raise ValueError("No such file: %s" % conf_fname)
            conf = NabuConfigParser(conf_fname).conf_dict
            self.nabu_config = validate_nabu_config(conf)
            self._create_logger(create_logger)
            dataset_infos = analyze_dataset(
                self.nabu_config["dataset"]["location"],
                processes_file=self.nabu_config["preproc"]["processes_file"],
                extra_options={
                    "force_flatfield": self.nabu_config["preproc"]["flatfield_enabled"] == "forced",
                    "exclude_projections": self.nabu_config["dataset"]["exclude_projections"],
                    "output_dir": self.nabu_config["output"]["location"],
                    "hdf5_entry": self.nabu_config["dataset"]["hdf5_entry"],
                },
                logger=self.logger
            )
        else:
            if (conf_dict is None) or (dataset_infos is None):
                raise ValueError(args_error_msg)
            self.nabu_config = validate_nabu_config(conf_dict)
            self._create_logger(create_logger)
            if not(isinstance(dataset_infos, DatasetAnalyzer)):
                raise ValueError("Expected a DatasetAnalyzer instance for dataset_infos")
        self.dataset_infos = dataset_infos
        self.checks = checks
        self.remove_unused_radios = remove_unused_radios
        self._get_cor()
        self.validation_stage2()
        self.build_processing_steps()


    def _create_logger(self, create_logger):
        if create_logger is False:
            self.logger = PrinterLogger()
            return
        elif create_logger is True:
            dataset_loc = self.nabu_config["dataset"]["location"]
            dataset_fname_rel = os.path.basename(dataset_loc)
            if os.path.isfile(dataset_loc):
                logger_filename = os.path.join(
                    os.path.abspath(os.getcwd()),
                    os.path.splitext(dataset_fname_rel)[0] + "_nabu.log"
                )
            else:
                logger_filename = os.path.join(
                    os.path.abspath(os.getcwd()),
                    dataset_fname_rel + "_nabu.log"
                )
        elif isinstance(create_logger, str):
            logger_filename = create_logger
        else:
            raise ValueError("Expected bool or str for create_logger")
        self.logger = Logger(
            "nabu",
            level=self.nabu_config["about"]["verbosity"],
            logfile=logger_filename
        )


    def _get_cor(self):
        cor = self.nabu_config["reconstruction"]["rotation_axis_position"]
        if isinstance(cor, str): # auto-CoR
            self.corfinder = CORFinder(
                self.dataset_infos,
                halftomo=self.nabu_config["reconstruction"]["enable_halftomo"],
                do_flatfield=self.nabu_config["preproc"]["flatfield_enabled"],
                cor_options=self.nabu_config["reconstruction"]["cor_options"],
                logger=self.logger
            )
            cor = self.corfinder.find_cor(search_method=cor)
        self.dataset_infos.axis_position = cor


    def validation_stage2(self):
        validator = NabuValidator(self.nabu_config, self.dataset_infos)
        if self.checks:
            validator.perform_all_checks(remove_unused_radios=self.remove_unused_radios)


    def build_processing_steps(self):
        """
        Build a list of processing steps from a ProcessConfig instance.
        The returned structures are a more compact and ready-to-use representation
        of the two main fields of ProcessConfig (dataset_infos and nabu_config).
        """
        nabu_config = self.nabu_config
        dataset_infos = self.dataset_infos
        binning = (nabu_config["dataset"]["binning"], nabu_config["dataset"]["binning_z"])
        tasks = []
        options = {}

        #
        # Dataset / Get data
        #
        # First thing to do is to get the data (radios or sinograms)
        # For now data is assumed to be on disk (see issue #66).
        tasks.append("read_chunk")
        options["read_chunk"] = {
            "files": dataset_infos.projections, # TODO handle sinograms
            "sub_region": None,
            "binning": binning,
            "dataset_subsampling": nabu_config["dataset"]["projections_subsampling"]
        }
        #
        # Flat-field
        #
        if nabu_config["preproc"]["flatfield_enabled"]:
            tasks.append("flatfield")
            options["flatfield"] = {
                #  ChunkReader handles binning/subsampling by itself,
                # but FlatField needs "real" indices (after binning/subsampling)
                "projs_indices": dataset_infos._projs_indices_subsampled,
                "binning": binning,
            }
        if nabu_config["preproc"]["ccd_filter_enabled"]:
            tasks.append("ccd_correction")
            options["ccd_correction"] = {
                "type": "median_clip", # only one available for now
                "median_clip_thresh": nabu_config["preproc"]["ccd_filter_threshold"],
            }
        #
        # Double flat field
        #
        if nabu_config["preproc"]["double_flatfield_enabled"]:
            tasks.append("double_flatfield")
            options["double_flatfield"] = {
                # ~ "results_location": nabu_config["output"]["location"], # not useful (?)
                "sigma": nabu_config["preproc"]["dff_sigma"],
            }
        #
        #
        # Phase retrieval
        #
        if nabu_config["phase"]["method"] != None:
            tasks.append("phase")
            options["phase"] = copy_dict_items(
                nabu_config["phase"],
                ["delta_beta", "margin", "padding_type"]
            )
            options["phase"].update({
                "energy_kev": dataset_infos.energy,
                "distance_cm": dataset_infos.distance * 1e2,
                "pixel_size_microns": dataset_infos.pixel_size,
            })
            if binning != (1, 1):
                options["phase"]["delta_beta"] /= (binning[0] * binning[1])
        #
        # Unsharp
        #
        if nabu_config["phase"]["unsharp_coeff"] > 0:
            tasks.append("unsharp_mask")
            options["unsharp_mask"] = copy_dict_items(
                nabu_config["phase"], ["unsharp_coeff", "unsharp_sigma"]
            )
        #
        # -logarithm
        #
        if nabu_config["preproc"]["take_logarithm"]:
            tasks.append("take_log")
            options["take_log"] = copy_dict_items(nabu_config["preproc"], ["log_min_clip", "log_max_clip"])
        #
        # Translation movements
        #
        translations = dataset_infos.translations
        if translations is not None:
            tasks.append("radios_movements")
            options["radios_movements"] = {
                "translation_movements": dataset_infos.translations
            }
        #
        # Sinogram normalization (before half-tomo)
        #
        if nabu_config["preproc"]["sino_normalization"] != None:
            tasks.append("sino_normalization")
            options["sino_normalization"] = {
                "method": nabu_config["preproc"]["sino_normalization"]
            }
        #
        # Reconstruction
        #
        if nabu_config["reconstruction"]["method"] != None:
            tasks.append("build_sino")
            options["build_sino"] = copy_dict_items(
                nabu_config["reconstruction"],
                ["rotation_axis_position", "enable_halftomo", "start_x", "end_x",
                 "start_y", "end_y", "start_z", "end_z"]
            )
            options["build_sino"]["axis_correction"] = dataset_infos.axis_correction
            tasks.append("reconstruction")
            # Iterative is not supported through configuration file for now.
            options["reconstruction"] = copy_dict_items(
                nabu_config["reconstruction"],
                ["method", "rotation_axis_position", "fbp_filter_type",
                "padding_type", "enable_halftomo",
                "start_x", "end_x", "start_y", "end_y", "start_z", "end_z"]
            )
            rec_options = options["reconstruction"]
            rec_options["rotation_axis_position"] = dataset_infos.axis_position
            options["build_sino"]["rotation_axis_position"] = dataset_infos.axis_position
            rec_options["axis_correction"] = dataset_infos.axis_correction
            rec_options["angles"] = dataset_infos.reconstruction_angles
            rec_options["radio_dims_y_x"] = dataset_infos.radio_dims[::-1]
            rec_options["pixel_size_cm"] = dataset_infos.pixel_size * 1e-4 # pix size is in microns
            if rec_options["enable_halftomo"]:
                rec_options["angles"] = rec_options["angles"][:rec_options["angles"].size//2]
                cor_i = int(round(rec_options["rotation_axis_position"]))
                # New keys
                rec_options["rotation_axis_position_halftomo"] = (2*cor_i-1)/2.
            # New key
            rec_options["cor_estimated_auto"] = isinstance(nabu_config["reconstruction"]["rotation_axis_position"], str)

        #
        # Histogram
        #
        if nabu_config["postproc"]["output_histogram"]:
            tasks.append("histogram")
            options["histogram"] = copy_dict_items(
                nabu_config["postproc"], ["histogram_bins"]
            )

        #
        # Save
        #
        if nabu_config["output"]["location"] is not None:
            tasks.append("save")
            options["save"] = copy_dict_items(
                nabu_config["output"], list(nabu_config["output"].keys())
            )
            options["save"]["overwrite"] = nabu_config["output"]["overwrite_results"]

        # "sub_region" is the same for all steps
        # ~ sub_region = options["read_chunk"]["sub_region"]
        # ~ for step in options.keys():
            # ~ options[step]["sub_region"] = sub_region

        self.processing_steps = tasks
        self.processing_options = options
