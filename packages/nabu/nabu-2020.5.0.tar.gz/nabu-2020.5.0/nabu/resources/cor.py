import numpy as np
from silx.io import get_data
from ..preproc.ccd import FlatField
from ..preproc.alignment import CenterOfRotation, CenterOfRotationAdaptiveSearch, CenterOfRotationSlidingWindow, CenterOfRotationGrowingWindow
from .logger import LoggerOrPrint
from .utils import extract_parameters
from ..utils import check_supported

class CORFinder:
    """
    An application-type class for finding the Center Of Rotation (COR).
    """

    search_methods = {
        "centered":{
            "class": CenterOfRotation,
        },
        "global": {
            "class": CenterOfRotationAdaptiveSearch,
            "default_kwargs": {"low_pass": 1, "high_pass":20},
        },
        "sliding-window": {
            "class": CenterOfRotationSlidingWindow,
            "default_args": ["center"],
        },
        "growing-window": {
            "class": CenterOfRotationGrowingWindow,
        }
    }

    def __init__(self, dataset_info, angles=None, halftomo=False, do_flatfield=True, cor_options=None, logger=None):
        """
        Initialize a CORFinder object.

        Parameters
        ----------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        angles: array, optional
            Information on rotation angles. If provided, it overwrites
            the rotation angles available in `dataset_info`, if any.
        halftomo: bool, optional
            Whether the scan was performed in "half tomography" acquisition.
        """
        self.logger = LoggerOrPrint(logger)
        self.halftomo = halftomo
        self.dataset_info = dataset_info
        self.do_flatfield = do_flatfield
        self.shape = dataset_info._radio_dims_notbinned[::-1]
        self._get_angles(angles)
        self._init_radios()
        self._init_flatfield()
        self._apply_flatfield()
        self._default_search_method = "centered"
        if self.halftomo:
            self._default_search_method = "global"
        self._get_cor_options(cor_options)


    def _get_angles(self, angles):
        dataset_angles = self.dataset_info.rotation_angles
        if dataset_angles is None:
            if angles is None: # should not happen with hdf5
                theta_min = 0
                theta_max = np.pi
                msg = "no information on angles was found for this dataset. Using default range "
                endpoint = False
                if self.halftomo:
                    theta_max *= 2
                    endpoint = True
                    msg += "[0, 360]"
                else:
                    msg += "[0, 180["
                self.logger.warning(msg)
                angles = np.linspace(
                    theta_min, theta_max, len(self.dataset_info.projections),
                    endpoint=endpoint
                )
            dataset_angles = angles
        self.angles = dataset_angles


    def _init_radios(self):
        # We take 2 radios. It could be tuned for a 360 degrees scan.
        self._n_radios = 2
        self._radios_indices = []
        radios_indices = sorted(self.dataset_info.projections.keys())

        # Take angles 0 and 180 degrees. It might not work of there is an offset
        i_0 = np.argmin(np.abs(self.angles))
        i_180 = np.argmin(np.abs(self.angles - np.pi))
        _min_indices = [i_0, i_180]
        self._radios_indices = [
            radios_indices[i_0],
            radios_indices[i_180]
        ]
        self.radios = np.zeros((self._n_radios, ) + self.shape, "f")
        for i in range(self._n_radios):
            radio_idx = self._radios_indices[i]
            self.radios[i] = get_data(self.dataset_info.projections[radio_idx]).astype("f")


    def _init_flatfield(self):
        if not(self.do_flatfield):
            return
        self.flatfield = FlatField(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self._radios_indices,
            interpolation="linear",
            convert_float=True
        )


    def _apply_flatfield(self):
        if not(self.do_flatfield):
            return
        self.flatfield.normalize_radios(self.radios)


    def _get_cor_options(self, cor_options):
        if cor_options is None:
            self.cor_options = None
            return
        try:
            cor_options = extract_parameters(cor_options)
        except Exception as exc:
            msg = "Could not extract parameters from cor_options: %s" % (str(exc))
            self.logger.fatal(msg)
            raise ValueError(msg)
        self.cor_options = cor_options


    def find_cor(self, search_method=None):
        """
        Find the center of rotation.

        Parameters
        ----------
        search_method: str, optional
            Which CoR search method to use. Default "centered".

        Returns
        -------
        cor: float
            The estimated center of rotation for the current dataset.

        Notes
        ------
        This function passes the named parameters to nabu.preproc.alignment.CenterOfRotation.find_shift.
        """
        search_method = search_method or self._default_search_method
        check_supported(search_method, self.search_methods.keys(), "CoR estimation method")
        cor_class = self.search_methods[search_method]["class"]
        cor_finder = cor_class(logger=self.logger)
        self.logger.info("Estimating center of rotation")

        default_params = self.search_methods[search_method].get("default_kwargs", None) or {}
        cor_exec_kwargs = default_params.copy()
        cor_exec_kwargs.update(self.cor_options or {})
        cor_exec_args = self.search_methods[search_method].get("default_args", None) or []
        # Specific to CenterOfRotationSlidingWindow
        if cor_class == CenterOfRotationSlidingWindow:
            side_param = cor_exec_kwargs.pop("side", "center")
            cor_exec_args = [side_param]
        #
        self.logger.debug("%s(%s)" % (get_class_name(cor_class), str(cor_exec_kwargs)))
        shift = cor_finder.find_shift(
            self.radios[0],
            np.fliplr(self.radios[1]),
            *cor_exec_args,
            **cor_exec_kwargs
        )
        # find_shift returned a single scalar in 2020.1
        # This should be the default after 2020.2 release
        if hasattr(shift, "__iter__"):
            shift = shift[0]
        #
        res = self.shape[1]/2 + shift
        self.logger.info("Estimated center of rotation: %.2f" % res)
        return res


def get_class_name(class_object):
    return str(class_object).split(".")[-1].strip(">").strip("'").strip('"')
