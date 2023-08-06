from os import path, mkdir
from ..resources.logger import LoggerOrPrint
from ..resources.utils import is_hdf5_extension
from ..utils import check_supported
from ..io.writer import Writers, NXProcessWriter
from ..io.utils import check_h5py_version # won't be necessary once h5py >= 3.0 required

#
# Decorators and callback mechanism
#

def use_options(step_name, step_attr):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if step_name not in self.processing_steps:
                self.__setattr__(step_attr, None)
                return
            self._steps_name2component[step_name] = step_attr
            self._steps_component2name[step_attr] = step_name
            return func(*args, **kwargs)
        return wrapper
    return decorator


def pipeline_step(step_attr, step_desc):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.__getattribute__(step_attr) is None:
                return
            self.logger.info(step_desc)
            res = func(*args, **kwargs)
            self.logger.debug("End " + step_desc)
            callback = self._callbacks.get(self._steps_component2name[step_attr], None)
            if callback is not None:
                callback(self)
            return res
        return wrapper
    return decorator


#
# Writer
#

class WriterConfigurator:
    def __init__(self, options, output_dir=None, start_index=None, logger=None, nx_info=None, write_histogram=False, histogram_entry="entry"):
        """
        Create a Writer from a set of parameters.

        Parameters
        ----------
        options: dict
            A dictionary of options for writer. Must have at least "file_format", "location"
            and "file_prefix" keys.
        output_dir: str, optional
            Directory where the file(s) will be written. If not provided, it will
            be set to options["location"].
        start_index: int, optional
            Index to start the files numbering (filename_0123.ext).
            Default is 0.
            Ignored for HDF5 extension.
        logger: nabu.resources.logger.Logger, optional
            Logger object
        nx_info: dict, optional
            Dictionary containing the nexus information.
        write_histogram: bool, optional
            Whether to also write a histogram of data. If set to True, it will configure
            an additional "writer".
        histogram_entry: str, optional
            Name of the HDF5 entry for the output histogram file, if write_histogram is True.
            Ignored if the output format is already HDF5 : in this case, nx_info["entry"] is taken.
        """
        self.logger = LoggerOrPrint(logger)
        self.options = options
        self.start_index = start_index
        self.write_histogram = write_histogram

        file_format = options["file_format"]
        check_supported(file_format, list(Writers.keys()), "output file format")

        self._set_output_dir(output_dir)
        self._set_file_name()

        # Init Writer
        writer_cls = Writers[file_format]
        writer_args = [self.fname]
        writer_kwargs = {}
        self._writer_exec_args = []
        self._writer_exec_kwargs = {}
        self._is_hdf5_output = is_hdf5_extension(file_format)

        if self._is_hdf5_output:
            writer_kwargs["entry"] = nx_info["entry"]
            writer_kwargs["filemode"] = "a"
            writer_kwargs["overwrite"] = self.options["overwrite"]
            self._writer_exec_args.append(nx_info["process_name"])
            self._writer_exec_kwargs["processing_index"] = nx_info["processing_index"]
            self._writer_exec_kwargs["config"] = nx_info["config"]
            check_h5py_version(self.logger)
        else:
            writer_kwargs["start_index"] = self.start_index
        self.writer = writer_cls(*writer_args, **writer_kwargs)

        if self.write_histogram and not(self._is_hdf5_output):
            self._init_separate_histogram_writer(histogram_entry)


    def _set_output_dir(self, output_dir):
        if output_dir is None:
            output_dir = path.join(
                self.options["location"],
                self._orig_file_prefix
            )
        self.output_dir = output_dir
        if path.exists(self.output_dir):
            if not(path.isdir(self.output_dir)):
                raise ValueError(
                    "Unable to create directory %s: already exists and is not a directory"
                    % self.output_dir
                )
        else:
            self.logger.debug("Creating directory %s" % self.output_dir)
            mkdir(self.output_dir)


    def _set_file_name(self):
        self.fname = path.join(
            self.output_dir,
            self.options["file_prefix"] + "." + self.options["file_format"]
        )
        if path.exists(self.fname):
            err = "File already exists: %s" % self.fname
            if self.options["overwrite"]:
                if self.options.get("warn_overwrite", True):
                    self.logger.warning(err + ". It will be overwritten as requested in configuration")
                    self.options["warn_overwrite"] = False
            else:
                self.logger.fatal(err)
                raise ValueError(err)


    def _init_separate_histogram_writer(self, hist_entry):
        hist_fname = path.join(
            self.output_dir,
            "histogram_%04d.hdf5" % self.start_index
        )
        self.histogram_writer = NXProcessWriter(
            hist_fname,
            entry=hist_entry,
            filemode="w",
            overwrite=True,
        )


    def get_histogram_writer(self):
        if not(self.write_histogram):
            return None
        if self._is_hdf5_output:
            return self.writer
        else:
             return self.histogram_writer
