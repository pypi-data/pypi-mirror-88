import os
import posixpath
from tempfile import mkdtemp
import numpy as np
from silx.io.url import DataUrl
from tomoscan.esrf.edfscan import EDFTomoScan
from tomoscan.esrf.hdf5scan import HDF5TomoScan
from ..thirdparty.tomwer_load_flats_darks import get_flats_frm_process_file, get_darks_frm_process_file
from .nxflatfield import NXFlatField
from ..utils import is_writeable
from .utils import is_hdf5_extension, get_values_from_file
from .logger import LoggerOrPrint


dataset_infos = {
    "num_radios": None,
    "num_darks": None,
    "num_flats": None,
    "radios": None,
    "darks": None,
    "flats": None,
    "frame_dims": None,
    "energy_kev": None,
    "distance_m": None,
    "pixel_size_microns": None,
}


class DatasetAnalyzer(object):
    """
    Base class for datasets analyzers.
    """
    def __init__(self, location, processes_file=None, extra_options=None, logger=None):
        """
        Initialize a Dataset analyzer.

        Parameters
        ----------
        location: str
            Dataset location (directory or file name)
        processes_file: str, optional
            Processes file providing supplementary information (ex. pre-processed data)
        extra_options: dict, optional
            Extra options on how to interpret the dataset.
            Available options are the following:
              - force_flatfield
              - output_dir
        logger: logging object, optional
            Logger. If not set, messages will just be printed in stdout.
        """
        self.logger = LoggerOrPrint(logger)
        self.location = location
        self.processes_file = processes_file
        self._set_extra_options(extra_options)
        self._get_excluded_projections()


    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {
            "force_flatfield": False,
            "output_dir": None,
            "exclude_projections": None,
            "hdf5_entry": None,
        }
        advanced_options.update(extra_options)
        self.extra_options = advanced_options

    def _get_excluded_projections(self):
        excluded_projs = self.extra_options["exclude_projections"]
        if excluded_projs is None:
            return
        projs_idx = get_values_from_file(excluded_projs, any_size=True).astype(np.int32).tolist()
        self.logger.info("Ignoring projections: %s" % (str(projs_idx)))
        self.extra_options["exclude_projections"] = projs_idx


    def _init_dataset_scan(self, filetype, **kwargs):
        scanners = {
            "edf": EDFTomoScan,
            "hdf5": HDF5TomoScan,
        }
        if filetype not in scanners.keys():
            raise ValueError("No scanner for file type: %s" % filetype)
        if filetype == "hdf5" and self.extra_options["hdf5_entry"] is not None:
            kwargs["entry"] = self.extra_options["hdf5_entry"]
        scanner = scanners[filetype]
        self.dataset_scanner = scanner(
            self.location,
            ignore_projections=self.extra_options["exclude_projections"],
            **kwargs
        )
        self.projections = self.dataset_scanner.projections
        self.flats = self.dataset_scanner.flats
        self.darks = self.dataset_scanner.darks
        self.n_angles = len(self.dataset_scanner.projections)
        self.radio_dims = (self.dataset_scanner.dim_1, self.dataset_scanner.dim_2)
        self._binning = (1, 1)
        self.translations = None
        self.axis_position = None
        self._radio_dims_notbinned = self.radio_dims

    @property
    def energy(self):
        """
        Return the energy in kev.
        """
        return self.dataset_scanner.energy

    @property
    def distance(self):
        """
        Return the sample-detector distance in meters.
        """
        return abs(self.dataset_scanner.distance)

    @property
    def pixel_size(self):
        """
        Return the pixel size in microns.
        """
        raise ValueError("Must be implemented by inheriting class")

    @property
    def binning(self):
        """
        Return the binning in (x, y)
        """
        return self._binning

    @property
    def rotation_angles(self):
        """
        Return the rotation angles in radians.
        """
        return self._get_rotation_angles()


    def remove_unused_radios(self):
        """
        Remove "unused" radios.
        This is used for legacy ESRF scans.
        """
        # This should only be used with EDF datasets
        if self.dataset_scanner.type != "edf":
            return
        # Extraneous projections are assumed to be on the end
        projs_indices = sorted(self.projections.keys())
        used_radios_range = range(projs_indices[0], self.dataset_scanner.tomo_n)
        radios_not_used = []
        for idx in self.projections.keys():
            if idx not in used_radios_range:
                radios_not_used.append(idx)
        for idx in radios_not_used:
            self.projections.pop(idx)
        return radios_not_used


class EDFDatasetAnalyzer(DatasetAnalyzer):
    """
    EDF Dataset analyzer for legacy ESRF acquisitions
    """
    def __init__(self, location, n_frames=1, processes_file=None, extra_options=None, logger=None):
        """
        EDF Dataset analyzer.

        Parameters
        -----------
        location: str
            Location of the folder containing EDF files
        """
        super().__init__(
            location, processes_file=processes_file, extra_options=extra_options, logger=logger
        )
        if not(os.path.isdir(location)):
            raise ValueError("%s is not a directory" % location)
        self._init_dataset_scan("edf", n_frames=n_frames)

    def _get_rotation_angles(self):
        # Not available in EDF dataset
        return None

    @property
    def pixel_size(self):
        """
        Return the pixel size in microns.
        """
        # TODO X and Y pixel size
        return self.dataset_scanner.pixel_size * 1e6


    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset.
        Not applicable for EDF (return None)
        """
        return None



class HDF5DatasetAnalyzer(DatasetAnalyzer):
    """
    HDF5 dataset analyzer
    """
    def __init__(self, location, processes_file=None, extra_options=None, logger=None):
        """
        HDF5 Dataset analyzer.

        Parameters
        -----------
        location: str
            Location of the HDF5 master file
        """
        super().__init__(
            location, processes_file=processes_file, extra_options=extra_options, logger=logger
        )
        if not(os.path.isfile(location)):
            raise ValueError("%s is not a file" % location)
        self._init_dataset_scan("hdf5")
        self._get_flats_darks()
        self._rot_angles = None


    def _get_flats_darks(self):
        if len(self.flats) == 0 and not(self.extra_options["force_flatfield"]):
            # No flats at all in the dataset. Do nothing.
            return
        if self.processes_file is None and self._load_flats_from_tomwer():
            # Loaded from tomwer_processes.h5
            return
        # Otherwise load or compute flats/darks with nabu
        self._compute_or_load_flats()


    def _load_flats_from_tomwer(self, tomwer_processes_fname=None):
        tomwer_processes_fname = tomwer_processes_fname or "tomwer_processes.h5"
        tomwer_processes_file = os.path.join(self.dataset_scanner.path, "tomwer_processes.h5")
        if not(os.path.isfile(tomwer_processes_file)):
            return False
        self.logger.info("Loading darks and refs from %s" % tomwer_processes_file)
        new_flats = get_flats_frm_process_file(
            tomwer_processes_file, self.dataset_scanner.entry
        )
        new_darks = get_darks_frm_process_file(
            tomwer_processes_file, self.dataset_scanner.entry
        )
        self.flats = new_flats
        self.darks = new_darks
        return True


    def _get_results_file(self):
        results_relfname = os.path.splitext(
            os.path.basename(self.dataset_scanner.master_file)
        )[0] + "_nabu_processes.hdf5"
        # Attempt 1: write in the same dir as the master NX file
        results_dir = os.path.dirname(self.dataset_scanner.master_file)
        if is_writeable(results_dir):
            return os.path.join(results_dir, results_relfname)
        # Attempt 2: write in the "output" dir, if specified
        out_dir = self.extra_options["output_dir"]
        if out_dir is not None and is_writeable(out_dir):
            return os.path.join(out_dir, results_relfname)
        # Last attempt: write in a temporary directory
        tempdir = mkdtemp(prefix="nabu_flatfield_")
        return os.path.join(tempdir, results_relfname)


    def _compute_or_load_flats(self):
        h5_entry = self.hdf5_entry or "entry"
        h5_path = posixpath.join(h5_entry, "flat_field_images")
        # In this case, we always want to return a dict of DataUrl,
        # so we have to write the final flats/darks somewhere.
        # Therefore results_url cannot be None when instantiating NXFlatField.
        # It will be ignored if data can be loaded from self.processes_file
        results_file = self._get_results_file()
        results_url = DataUrl(file_path=results_file, data_path=h5_path)

        lookup_files = None
        if self.processes_file is not None:
            lookup_files = [DataUrl(file_path=self.processes_file, data_path=h5_path)]
        else:
            if os.path.isfile(results_file):
                # We use an existing "results file"  as lookup file.
                # NXFlatField wont overwrite it if it has the good configuration
                lookup_files = [DataUrl(file_path=results_file, data_path=h5_path)]

        self._nxflatfield = NXFlatField(
            self._get_dataset_hdf5_url(),
            self.dataset_scanner.image_key,
            lookup_files=lookup_files,
            results_url=results_url,
            force_load_existing_results=self.extra_options["force_flatfield"],
            flats_reduction="median",
            darks_reduction="mean",
            logger=self.logger
        )
        res = self._nxflatfield.get_final_urls()
        self.flats = res["flats"]
        self.darks = res["darks"]


    def _get_rotation_angles(self):
        if self._rot_angles is None:
            angles = np.array(self.dataset_scanner.rotation_angle)
            projs_idx = np.array(list(self.projections.keys()))
            angles = angles[projs_idx]
            self._rot_angles = np.deg2rad(angles)
        return self._rot_angles


    def _get_dataset_hdf5_url(self):
        first_proj_idx = sorted(self.projections.keys())[0]
        first_proj_url = self.projections[first_proj_idx]
        return DataUrl(
            file_path=first_proj_url.file_path(),
            data_path=first_proj_url.data_path(),
            data_slice=None
        )


    @property
    def dataset_hdf5_url(self):
        return self._get_dataset_hdf5_url()


    @property
    def pixel_size(self):
        """
        Return the pixel size in microns.
        """
        # TODO X and Y pixel size
        try:
            xs, yz = self.dataset_scanner._get_x_y_magnified_pixel_values()
            ps = xs * 1e6
        except:
            ps = self.dataset_scanner.pixel_size * 1e6
        return ps


    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset
        """
        return self.dataset_scanner.entry




def analyze_dataset(dataset_path, processes_file=None, extra_options=None, logger=None):
    if not(os.path.isdir(dataset_path)):
        if not(os.path.isfile(dataset_path)):
            raise ValueError("Error: %s no such file or directory" % dataset_path)
        if not(is_hdf5_extension(os.path.splitext(dataset_path)[-1].replace(".", ""))):
            raise ValueError("Error: expected a HDF5 file")
        dataset_analyzer_class = HDF5DatasetAnalyzer
    else: # directory -> assuming EDF
        dataset_analyzer_class = EDFDatasetAnalyzer
    dataset_structure = dataset_analyzer_class(
        dataset_path,
        processes_file=processes_file,
        extra_options=extra_options,
        logger=logger
    )
    return dataset_structure

