from glob import glob
from os import path, getcwd, chdir
from datetime import datetime
import numpy as np
from h5py import VirtualSource, VirtualLayout
from tomoscan.io import HDF5File
from silx.utils.enum import Enum
from silx.third_party.TiffIO import TiffIO
from .. import version
from ..misc.utils import rescale_data
from .config import export_dict_to_h5
from .utils import check_h5py_version # won't be necessary once h5py >= 3.0 required

try:
    from glymur import Jp2k
    __have_jp2k__ = True
except ImportError:
    __have_jp2k__ = False


def get_datetime():
    """
    Function used by some writers to indicate the current date.
    """
    return datetime.now().replace(microsecond=0).isoformat()


class Writer:
    """
    Base class for all writers.
    """
    def __init__(self, fname):
        self.fname = fname


    def get_filename(self):
        return self.fname


class NXProcessWriter(Writer):
    def __init__(self, fname, entry=None, filemode="a", overwrite=False):
        """
        Initialize a NXProcessWriter.

        Parameters
        -----------
        fname: str
            Path to the HDF5 file.
        entry: str, optional
            Entry in the HDF5 file. Default is "entry"
        """
        super().__init__(fname)
        self._set_entry(entry)
        self._filemode = filemode
        self.overwrite = overwrite
        check_h5py_version()


    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = "/".join([self.entry])
        if not(data_path.startswith("/")):
            data_path = "/" + data_path
        self.data_path = data_path


    def write(self, result, process_name, processing_index=0, config=None, is_frames_stack=True):
        """
        Write the result in the current NXProcess group.

        Parameters
        ----------
        result: numpy.ndarray
            Array containing the processing result
        process_name: str
            Name of the processing
        processing_index: int
            Index of the processing (in a pipeline)
        config: dict, optional
            Dictionary containing the configuration.
        """
        with HDF5File(self.fname, self._filemode, swmr=True) as fid:
            results_path = path.join(self.data_path, process_name)
            if self.overwrite and results_path in fid:
                del fid[results_path]
            nx_entry = fid.require_group(self.data_path)
            if "NX_class" not in nx_entry.attrs:
                nx_entry.attrs["NX_class"] = "NXentry"

            nx_process = nx_entry.require_group(process_name)
            nx_process.attrs['NX_class'] = "NXprocess"

            nx_process['program'] = "nabu"
            nx_process['version'] = version
            nx_process['date'] = get_datetime()
            nx_process['sequence_index'] = np.int32(processing_index)

            if config is not None:
                export_dict_to_h5(
                    config,
                    self.fname,
                    '/'.join([nx_process.name, 'configuration']),
                    overwrite_data=True,
                    mode="a"
                )
                nx_process['configuration'].attrs['NX_class'] = "NXcollection"
            if isinstance(result, dict):
                results_path = '/'.join([nx_process.name, 'results'])
                export_dict_to_h5(
                    result,
                    self.fname,
                    results_path,
                    overwrite_data=True,
                    mode="a"
                )
            else:
                nx_data = nx_process.require_group('results')
                results_path = nx_data.name
                nx_data.attrs['NX_class'] = "NXdata"
                nx_data.attrs['signal'] = "data"
                if isinstance(result, VirtualLayout):
                    nx_data.create_virtual_dataset("data", result)
                else: # assuming array-like
                    nx_data['data'] = result
                if is_frames_stack:
                    nx_data['data'].attrs['interpretation'] = "image"

            # prepare the direct access plots
            nx_process.attrs['default'] = 'results'
            if "default" not in nx_entry.attrs:
                nx_entry.attrs["default"] = '/'.join([nx_process.name, 'results'])
            # Return the internal path to "results"
            return results_path


def merge_hdf5_files(
    files_or_pattern, h5_path, output_file, process_name,
    output_entry=None, output_filemode="a",
    processing_index=0, config=None, base_dir=None,
    overwrite=False
):
    """
    Parameters
    -----------
    files_or_pattern: str or list
        A list of file names, or a wildcard pattern.
        If a list is provided, it will not be sorted! This will have to be
        done before calling this function.
    h5_path: str
        Path inside the HDF5 input file(s)
    output_file: str
        Path of the output file
    process_name: str
        Name of the process
    output_entry: str, optional
        Output HDF5 root entry (default is "/entry")
    output_filemode: str, optional
        File mode for output file. Default is "a" (append)
    processing_index: int, optional
        Processing index for the output file. Default is 0.
    config: dict, optional
        Dictionary describing the configuration needed to get the results.
    base_dir: str, optional
        Base directory when using relative file names.
    overwrite: bool, optional
        Whether to overwrite already existing data in the final file.
        Default is False.
    """
    prev_cwd = None
    if base_dir is not None:
        prev_cwd = getcwd()
        chdir(base_dir)
    if isinstance(files_or_pattern, str):
        files_list = glob(files_or_pattern)
        files_list.sort()
    else: # list
        files_list = files_or_pattern
    if files_list == []:
        raise ValueError("Nothing found as pattern %s" % files_or_pattern)
    virtual_sources = []
    shapes = []
    for fname in files_list:
        with HDF5File(fname, "r", swmr=True) as fid:
            shape = fid[h5_path].shape
        vsource = VirtualSource(fname, name=h5_path, shape=shape)
        virtual_sources.append(vsource)
        shapes.append(shape)

    n_images = sum([shape[0] for shape in shapes])
    virtual_layout = VirtualLayout(
        shape=(n_images, ) + shapes[0][1:],
        dtype='f'
    )
    start_idx = 0
    for vsource, shape in zip(virtual_sources, shapes):
        n_imgs = shape[0]
        virtual_layout[start_idx:start_idx + n_imgs] = vsource
        start_idx += n_imgs
    nx_file = NXProcessWriter(
        output_file,
        entry=output_entry, filemode=output_filemode, overwrite=overwrite
    )
    nx_file.write(
        virtual_layout,
        process_name,
        processing_index=processing_index,
        config=config,
        is_frames_stack=True
    )
    if base_dir is not None:
        chdir(prev_cwd)


class TIFFWriter(Writer):
    def __init__(self, fname, multiframe=False, start_index=0, filemode="wb"):
        """
        Tiff writer.

        Parameters
        -----------
        fname: str
            Path to the output file name
        multiframe: bool, optional
            Whether to write all data in one single file. Default is
        start_index: int, optional
            When writing a stack of images, each image is written in a dedicated file
            (unless multiframe is set to True).
            In this case, the output is a series of files `filename_0000.tif`,
            `filename_0001.tif`, etc. This parameter is the starting index for
            file names.
            This option is ignored when multiframe is True.

        Notes
        ------
        If multiframe is False (default), then each image will be written in a
        dedicated tiff file.
        """
        super().__init__(fname)
        self.multiframe = multiframe
        self.filemode = filemode
        self.start_index = start_index


    def _write_tiff(self, data, config=None, filename=None, filemode=None):
        if filename is None:
            filename = self.fname
        if filemode is None:
            filemode = self.filemode
        tif = TiffIO(filename, mode=filemode)
        tif.writeImage(
            data,
            software=str("nabu %s" % version),
            info=config,
            date=get_datetime()
        )
        tif = None


    def write(self, data, *args, config=None, **kwargs):
        if data.ndim < 3:
            self._write_tiff(data, config=config)
            return
        if (data.ndim == 3) and (data.shape[0] == 1):
            self._write_tiff(data[0], config=config)
            return
        if self.multiframe:
            self._write_tiff(data[0], config=config)
            for i in range(1, data.shape[0]):
                self._write_tiff(data[i], config=config, filemode="rb+") # ?!
        else:
            dirname, rel_filename = path.split(self.fname)
            prefix, ext = path.splitext(rel_filename)
            for i in range(data.shape[0]):
                curr_rel_filename = prefix + str("_%04d" % (self.start_index + i)) + ext
                fname = path.join(dirname, curr_rel_filename)
                self._write_tiff(data[i], filename=fname, config=config)

    def get_filename(self):
        if self.multiframe:
            return self.fname
        else:
            return path.dirname(self.fname)


class JP2Writer(Writer):
    def __init__(self, fname, start_index=0, filemode="wb", psnr=None, auto_convert=True):
        """
        JPEG2000 writer. This class requires the python package `glymur` and the
        library `libopenjp2`.

        Parameters
        -----------
        fname: str
            Path to the output file name
        start_index: int, optional
            When writing a stack of images, each image is written in a dedicated file
            The output is a series of files `filename_0000.tif`, `filename_0001.tif`, etc.
            This parameter is the starting index for file names.
        psnr: list of int, optional
            The PSNR (Peak Signal-to-Noise ratio) for each jpeg2000 layer.
            This defines a quality metric for lossy compression.
            The number "0" stands for lossless compression.
        auto_convert: bool, optional
            Whether to automatically cast floating point data to uint16.
            Default is True.
        """
        super().__init__(fname)
        if not(__have_jp2k__):
            raise ValueError("Need glymur python package and libopenjp2 library")
        self.filemode = filemode
        self.start_index = start_index
        self.auto_convert = auto_convert
        if psnr is not None and np.isscalar(psnr):
            psnr = [psnr]
        self.psnr = psnr
        self._vmin = None
        self._vmax = None


    def _write_jp2k(self, data, filename=None):
        if filename is None:
            filename = self.fname
        # TODO this will have to change in future versions
        if data.dtype != np.uint16 and self.auto_convert:
            data = rescale_data(data, 0, 65535, data_min=self._vmin, data_max=self._vmax)
            data = data.astype(np.uint16)
        #
        jp2 = Jp2k(filename, data=data, psnr=self.psnr)


    def write(self, data, *args, **kwargs):
        if data.ndim < 3:
            self._write_jp2k(data)
            return
        if (data.ndim == 3) and (data.shape[0] == 1):
            self._write_jp2k(data[0])
            return
        dirname, rel_filename = path.split(self.fname)
        prefix, ext = path.splitext(rel_filename)
        for i in range(data.shape[0]):
            curr_rel_filename = prefix + str("_%04d" % (self.start_index + i)) + ext
            fname = path.join(dirname, curr_rel_filename)
            self._write_jp2k(data[i], filename=fname)


    def get_filename(self):
        return path.dirname(self.fname)


class NPYWriter(Writer):
    def __init__(self,  fname):
        super().__init__(fname)

    def write(self, result, *args, **kwargs):
        np.save(self.fname, result)


class NPZWriter(Writer):
    def __init__(self,  fname):
        super().__init__(fname)

    def write(self, result, *args, **kwargs):
        save_args = {"result": result}
        config = kwargs.get("config", None)
        if config is not None:
            save_args["configuration"] = config
        np.savez(self.fname, **save_args)


Writers = {
    "h5": NXProcessWriter,
    "hdf5": NXProcessWriter,
    "nx": NXProcessWriter,
    "nexus": NXProcessWriter,
    "npy": NPYWriter,
    "npz": NPZWriter,
    "tif": TIFFWriter,
    "tiff": TIFFWriter,
    "j2k": JP2Writer,
    "jp2": JP2Writer,
    "jp2k": JP2Writer,
}

