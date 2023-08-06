import math
import logging
import numpy as np
from numpy.polynomial.polynomial import Polynomial, polyval
from ..utils import previouspow2
from ..misc import fourier_filters
from ..resources.logger import LoggerOrPrint

try:
    from scipy.ndimage.filters import median_filter
    import scipy.fft

    local_fftn = scipy.fft.rfftn
    local_ifftn = scipy.fft.irfftn
    __have_scipy__ = True
except ImportError:
    from silx.math.medianfilter import medfilt2d as median_filter
    from silx.math.medianfilter import medfilt1d as median_filter_1d

    local_fftn = np.fft.fftn
    local_ifftn = np.fft.ifftn
    __have_scipy__ = False
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    __have_matplotlib__ = True
except ImportError:
    logging.getLogger(__name__).warning("Matplotlib not available. Plotting disabled")
    __have_matplotlib__ = False

try:
    from tqdm import tqdm

    def progress_bar(x, verbose=True):
        if verbose:
            return tqdm(x)
        else:
            return x


except ImportError:

    def progress_bar(x, verbose=True):
        return x


# possible values of the validity check
UNCHECKED_VALUE = -1
VALID_VALUE = 1
INVALID_VALUE = 0


class AlignmentBase(object):
    def __init__(
        self, vert_fft_width=False, horz_fft_width=False, verbose=False, logger=None, data_type=np.float32,
    ):
        """
        Alignment basic functions.

        Parameters
        ----------
        vert_fft_width: boolean, optional
            If True, restrict the vertical size to a power of 2:

            >>> new_v_dim = 2 ** math.floor(math.log2(v_dim))

        horz_fft_width: boolean, optional
            If True, restrict the horizontal size to a power of 2:

            >>> new_h_dim = 2 ** math.floor(math.log2(h_dim))

        verbose: boolean, optional
            When True it will produce verbose output, including plots.
        data_type: `numpy.float32`
            Computation data type.
        """

        self._check_result = UNCHECKED_VALUE

        self._init_parameters(vert_fft_width, horz_fft_width, verbose, logger, data_type)

    @property
    def check_result(self):
        return self._check_result

    @check_result.setter
    def check_result(self, value):
        if value not in [UNCHECKED_VALUE, VALID_VALUE, INVALID_VALUE]:
            raise ValueError(
                "The possible value that can be assigned to check_result are %d %d and %d"
                % (UNCHECKED_VALUE, VALID_VALUE, INVALID_VALUE)
            )
        self._check_result = value

    def _init_parameters(self, vert_fft_width, horz_fft_width, verbose, logger, data_type):
        self.truncate_vert_pow2 = vert_fft_width
        self.truncate_horz_pow2 = horz_fft_width

        if verbose and not __have_matplotlib__:
            self.logger.warning("Matplotlib not available. Plotting disabled, despite being activated by user")
            verbose = False
        self.verbose = verbose
        self.logger = LoggerOrPrint(logger)
        self.data_type = data_type

    @staticmethod
    def _check_img_stack_size(img_stack: np.ndarray, img_pos: np.ndarray):
        shape_stack = np.squeeze(img_stack).shape
        shape_pos = np.squeeze(img_pos).shape
        if not len(shape_stack) == 3:
            raise ValueError(
                "A stack of 2-dimensional images is required. Shape of stack: %s" % (" ".join(("%d" % x for x in shape_stack)))
            )
        if not len(shape_pos) == 1:
            raise ValueError(
                "Positions need to be a 1-dimensional array. Shape of the positions variable: %s"
                % (" ".join(("%d" % x for x in shape_pos)))
            )
        if not shape_stack[0] == shape_pos[0]:
            raise ValueError(
                "The same number of images and positions is required."
                + " Shape of stack: %s, shape of positions variable: %s"
                % (" ".join(("%d" % x for x in shape_stack)), " ".join(("%d" % x for x in shape_pos)),)
            )

    @staticmethod
    def _check_img_pair_sizes(img_1: np.ndarray, img_2: np.ndarray):
        shape_1 = np.squeeze(img_1).shape
        shape_2 = np.squeeze(img_2).shape
        if not len(shape_1) == 2:
            raise ValueError("Images need to be 2-dimensional. Shape of image #1: %s" % (" ".join(("%d" % x for x in shape_1))))
        if not len(shape_2) == 2:
            raise ValueError("Images need to be 2-dimensional. Shape of image #2: %s" % (" ".join(("%d" % x for x in shape_2))))
        if not np.all(shape_1 == shape_2):
            raise ValueError(
                "Images need to be of the same shape. Shape of image #1: %s, image #2: %s"
                % (" ".join(("%d" % x for x in shape_1)), " ".join(("%d" % x for x in shape_2)),)
            )

    @staticmethod
    def refine_max_position_2d(f_vals: np.ndarray, fy=None, fx=None):
        """Computes the sub-pixel max position of the given function sampling.

        Parameters
        ----------
        f_vals: numpy.ndarray
            Function values of the sampled points
        fy: numpy.ndarray, optional
            Vertical coordinates of the sampled points
        fx: numpy.ndarray, optional
            Horizontal coordinates of the sampled points

        Raises
        ------
        ValueError
            In case position and values do not have the same size, or in case
            the fitted maximum is outside the fitting region.

        Returns
        -------
        tuple(float, float)
            Estimated (vertical, horizontal) function max, according to the
            coordinates in fy and fx.
        """
        if not (len(f_vals.shape) == 2):
            raise ValueError(
                "The fitted values should form a 2-dimensional array. Array of shape: [%s] was given."
                % (" ".join(("%d" % s for s in f_vals.shape)))
            )
        if fy is None:
            fy_half_size = (f_vals.shape[0] - 1) / 2
            fy = np.linspace(-fy_half_size, fy_half_size, f_vals.shape[0])
        elif not (len(fy.shape) == 1 and np.all(fy.size == f_vals.shape[0])):
            raise ValueError(
                "Vertical coordinates should have the same length as values matrix. Sizes of fy: %d, f_vals: [%s]"
                % (fy.size, " ".join(("%d" % s for s in f_vals.shape)))
            )
        if fx is None:
            fx_half_size = (f_vals.shape[1] - 1) / 2
            fx = np.linspace(-fx_half_size, fx_half_size, f_vals.shape[1])
        elif not (len(fx.shape) == 1 and np.all(fx.size == f_vals.shape[1])):
            raise ValueError(
                "Horizontal coordinates should have the same length as values matrix. Sizes of fx: %d, f_vals: [%s]"
                % (fx.size, " ".join(("%d" % s for s in f_vals.shape)))
            )

        fy, fx = np.meshgrid(fy, fx, indexing="ij")
        fy = fy.flatten()
        fx = fx.flatten()
        coords = np.array([np.ones(f_vals.size), fy, fx, fy * fx, fy ** 2, fx ** 2])

        coeffs = np.linalg.lstsq(coords.T, f_vals.flatten(), rcond=None)[0]

        # For a 1D parabola `f(x) = ax^2 + bx + c`, the vertex position is:
        # x_v = -b / 2a. For a 2D parabola, the vertex position is:
        # (y, x)_v = - b / A, where:
        A = [[2 * coeffs[4], coeffs[3]], [coeffs[3], 2 * coeffs[5]]]
        b = coeffs[1:3]
        vertex_yx = np.linalg.lstsq(A, -b, rcond=None)[0]

        vertex_min_yx = [np.min(fy), np.min(fx)]
        vertex_max_yx = [np.max(fy), np.max(fx)]
        if np.any(vertex_yx < vertex_min_yx) or np.any(vertex_yx > vertex_max_yx):
            raise ValueError(
                "Fitted (y: {}, x: {}) positions are outside the input margins y: [{}, {}], and x: [{}, {}]".format(
                    vertex_yx[0], vertex_yx[1], vertex_min_yx[0], vertex_max_yx[0], vertex_min_yx[1], vertex_max_yx[1],
                )
            )
        return vertex_yx

    @staticmethod
    def refine_max_position_1d(f_vals, fx=None, return_vertex_val=False):
        """Computes the sub-pixel max position of the given function sampling.

        Parameters
        ----------
        f_vals: numpy.ndarray
            Function values of the sampled points
        fx: numpy.ndarray, optional
            Coordinates of the sampled points
        return_vertex_val: boolean, option
            Enables returning the vertex values. Defaults to False.

        Raises
        ------
        ValueError
            In case position and values do not have the same size, or in case
            the fitted maximum is outside the fitting region.

        Returns
        -------
        float
            Estimated function max, according to the coordinates in fx.
        """
        if not len(f_vals.shape) in (1, 2):
            raise ValueError(
                "The fitted values should be either one or a collection of 1-dimensional arrays. Array of shape: [%s] was given."
                % (" ".join(("%d" % s for s in f_vals.shape)))
            )
        num_vals = f_vals.shape[0]

        if fx is None:
            fx_half_size = (num_vals - 1) / 2
            fx = np.linspace(-fx_half_size, fx_half_size, num_vals)
        else:
            fx = np.squeeze(fx)
            if not (len(fx.shape) == 1 and np.all(fx.size == num_vals)):
                raise ValueError(
                    "Base coordinates should have the same length as values array. Sizes of fx: %d, f_vals: %d"
                    % (fx.size, num_vals)
                )

        if len(f_vals.shape) == 1:
            # using Polynomial.fit, because supposed to be more numerically
            # stable than previous solutions (according to numpy).
            poly = Polynomial.fit(fx, f_vals, deg=2)
            coeffs = poly.convert().coef
        else:
            coords = np.array([np.ones(num_vals), fx, fx ** 2])
            coeffs = np.linalg.lstsq(coords.T, f_vals, rcond=None)[0]

        # For a 1D parabola `f(x) = c + bx + ax^2`, the vertex position is:
        # x_v = -b / 2a.
        vertex_x = -coeffs[1, :] / (2 * coeffs[2, :])

        vertex_min_x = np.min(fx)
        vertex_max_x = np.max(fx)
        lower_bound_ok = vertex_min_x < vertex_x
        upper_bound_ok = vertex_x < vertex_max_x
        if not np.all(lower_bound_ok * upper_bound_ok):
            if len(f_vals.shape) == 1:
                message = "Fitted position {} is outide the input margins [{}, {}]".format(vertex_x, vertex_min_x, vertex_max_x)
            else:
                message = "Fitted positions outide the input margins [{}, {}]: %d below and %d above".format(
                    vertex_min_x, vertex_max_x, np.sum(1 - lower_bound_ok), np.sum(1 - upper_bound_ok),
                )
            raise ValueError(message)
        if return_vertex_val:
            vertex_val = coeffs[0, :] + vertex_x * coeffs[1, :] / 2
            return vertex_x, vertex_val
        else:
            return vertex_x

    @staticmethod
    def extract_peak_region_2d(cc, peak_radius=1, cc_vs=None, cc_hs=None):
        """
        Extracts a region around the maximum value.

        Parameters
        ----------
        cc: numpy.ndarray
            Correlation image.
        peak_radius: int, optional
            The l_inf radius of the area to extract around the peak. The default is 1.
        cc_vs: numpy.ndarray, optional
            The vertical coordinates of `cc`. The default is None.
        cc_hs: numpy.ndarray, optional
            The horizontal coordinates of `cc`. The default is None.

        Returns
        -------
        f_vals: numpy.ndarray
            The extracted function values.
        fv: numpy.ndarray
            The vertical coordinates of the extracted values.
        fh: numpy.ndarray
            The horizontal coordinates of the extracted values.
        """
        img_shape = np.array(cc.shape)
        # get pixel having the maximum value of the correlation array
        pix_max_corr = np.argmax(cc)
        pv, ph = np.unravel_index(pix_max_corr, img_shape)

        # select a n x n neighborhood for the sub-pixel fitting (with wrapping)
        pv = np.arange(pv - peak_radius, pv + peak_radius + 1) % img_shape[-2]
        ph = np.arange(ph - peak_radius, ph + peak_radius + 1) % img_shape[-1]

        # extract the (v, h) pixel coordinates
        fv = None if cc_vs is None else cc_vs[pv]
        fh = None if cc_hs is None else cc_hs[ph]

        # extract the correlation values
        pv, ph = np.meshgrid(pv, ph, indexing="ij")
        f_vals = cc[pv, ph]

        return (f_vals, fv, fh)

    @staticmethod
    def extract_peak_regions_1d(cc, axis=-1, peak_radius=1, cc_coords=None):
        """
        Extracts a region around the maximum value.

        Parameters
        ----------
        cc: numpy.ndarray
            Correlation image.
        axis: int, optional
            Find the max values along the specified direction. The default is -1.
        peak_radius: int, optional
            The l_inf radius of the area to extract around the peak. The default is 1.
        cc_coords: numpy.ndarray, optional
            The coordinates of `cc` along the selected axis. The default is None.

        Returns
        -------
        f_vals: numpy.ndarray
            The extracted function values.
        fc_ax: numpy.ndarray
            The coordinates of the extracted values, along the selected axis.
        """
        if len(cc.shape) == 1:
            cc = cc[None, ...]
        img_shape = np.array(cc.shape)
        if not (len(img_shape) == 2):
            raise ValueError(
                "The input image should be either a 1 or 2-dimensional array. Array of shape: [%s] was given."
                % (" ".join(("%d" % s for s in cc.shape)))
            )
        other_axis = (axis + 1) % 2
        # get pixel having the maximum value of the correlation array
        pix_max = np.argmax(cc, axis=axis)

        # select a n neighborhood for the many 1D sub-pixel fittings (with wrapping)
        p_ax_range = np.arange(-peak_radius, +peak_radius + 1)
        p_ax = (pix_max[None, :] + p_ax_range[:, None]) % img_shape[axis]

        p_ln = np.tile(np.arange(0, img_shape[other_axis])[None, :], [2 * peak_radius + 1, 1])

        # extract the pixel coordinates along the axis
        fc_ax = None if cc_coords is None else cc_coords[p_ax.flatten()].reshape(p_ax.shape)

        # extract the correlation values
        if other_axis == 0:
            f_vals = cc[p_ln, p_ax]
        else:
            f_vals = cc[p_ax, p_ln]

        return (f_vals, fc_ax)

    def _determine_roi(self, img_shape, roi_yxhw):
        if roi_yxhw is None:
            # vertical and horizontal window sizes are reduced to a power of 2
            # to accelerate fft if requested. Default is not.
            roi_yxhw = previouspow2(img_shape)
            if not self.truncate_vert_pow2:
                roi_yxhw[0] = img_shape[0]
            if not self.truncate_horz_pow2:
                roi_yxhw[1] = img_shape[1]

        roi_yxhw = np.array(roi_yxhw, dtype=np.int)
        if len(roi_yxhw) == 2:  # Convert centered 2-element roi into 4-element
            roi_yxhw = np.concatenate(((img_shape - roi_yxhw) // 2, roi_yxhw))
        return roi_yxhw

    def _prepare_image(
        self, img, invalid_val=1e-5, roi_yxhw=None, median_filt_shape=None, low_pass=None, high_pass=None,
    ):
        """
        Prepare and returns  a cropped  and filtered image, or array of filtered images if the input is an  array of images.

        Parameters
        ----------
        img: numpy.ndarray
            image or stack of images
        invalid_val: float
            value to be used in replacement of nan and inf values
        median_filt_shape: int or sequence of int
            the width or the widths of the median window
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`

        Returns
        -------
        numpy.array_like
            The computed filter
        """
        img = np.squeeze(img)  # Removes singleton dimensions, but does a shallow copy
        img = np.ascontiguousarray(img, dtype=self.data_type)

        if roi_yxhw is not None:
            img = img[
                ..., roi_yxhw[0] : roi_yxhw[0] + roi_yxhw[2], roi_yxhw[1] : roi_yxhw[1] + roi_yxhw[3],
            ]

        img = img.copy()

        img[np.isnan(img)] = invalid_val
        img[np.isinf(img)] = invalid_val

        if high_pass is not None or low_pass is not None:
            img_filter = fourier_filters.get_bandpass_filter(
                img.shape[-2:],
                cutoff_lowpass=low_pass,
                cutoff_highpass=high_pass,
                use_rfft=__have_scipy__,
                data_type=self.data_type,
            )
            # fft2 and iff2 use axes=(-2, -1) by default
            img = local_ifftn(local_fftn(img, axes=(-2, -1)) * img_filter, axes=(-2, -1)).real

        if median_filt_shape is not None:
            img_shape = img.shape
            if __have_scipy__:
                # expanding filter shape with ones, to cover the stack of images
                # but disabling inter-image filtering
                median_filt_shape = np.concatenate(
                    (np.ones((len(img_shape) - len(median_filt_shape),), dtype=np.int), median_filt_shape,)
                )
                img = median_filter(img, size=median_filt_shape)
            else:
                if len(img_shape) == 2:
                    img = median_filter(img, kernel_size=median_filt_shape)
                elif len(img_shape) > 2:
                    # if dealing with a stack of images, we have to do them one by one
                    img = np.reshape(img, (-1,) + tuple(img_shape[-2:]))
                    for ii in range(img.shape[0]):
                        img[ii, ...] = median_filter(img[ii, ...], kernel_size=median_filt_shape)
                    img = np.reshape(img, img_shape)

        return img

    def _compute_correlation_fft(self, img_1, img_2, padding_mode, axes=(-2, -1), low_pass=None, high_pass=None):
        do_circular_conv = padding_mode is None or padding_mode == "wrap"
        img_shape = img_2.shape
        if not do_circular_conv:
            pad_size = np.ceil(np.array(img_shape) / 2).astype(np.int)
            pad_array = [(0,)] * len(img_shape)
            for a in axes:
                pad_array[a] = (pad_size[a],)

            img_1 = np.pad(img_1, pad_array, mode=padding_mode)
            img_2 = np.pad(img_2, pad_array, mode=padding_mode)

        # compute fft's of the 2 images
        img_fft_1 = local_fftn(img_1, axes=axes)
        img_fft_2 = np.conjugate(local_fftn(img_2, axes=axes))

        img_prod = img_fft_1 * img_fft_2

        if low_pass is not None or high_pass is not None:
            filt = fourier_filters.get_bandpass_filter(
                img_shape[-2:],
                cutoff_lowpass=low_pass,
                cutoff_highpass=high_pass,
                use_rfft=__have_scipy__,
                data_type=self.data_type,
            )
            img_prod *= filt

        # inverse fft of the product to get cross_correlation of the 2 images
        cc = np.real(local_ifftn(img_prod, axes=axes))

        if not do_circular_conv:
            cc = np.fft.fftshift(cc, axes=axes)

            slicing = [slice(None)] * len(img_shape)
            for a in axes:
                slicing[a] = slice(pad_size[a], cc.shape[a] - pad_size[a])
            cc = cc[tuple(slicing)]

            cc = np.fft.ifftshift(cc, axes=axes)

        return cc


class CenterOfRotation(AlignmentBase):
    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Find the Center of Rotation (CoR), given two images.

        This method finds the half-shift between two opposite images, by
        means of correlation computed in Fourier space.

        The output of this function, allows to compute motor movements for
        aligning the sample rotation axis. Given the following values:

        - L1: distance from source to motor
        - L2: distance from source to detector
        - ps: physical pixel size
        - v: output of this function

        displacement of motor = (L1 / L2 * ps) * v

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`

        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        float
            Estimated center of rotation position from the center of the RoI in pixels.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... CoR_calc = CenterOfRotation()
        ... cor_position = CoR_calc.find_shift(radio1, radio2)

        Or for noisy images:

        >>> cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))
        """

        self.check_result = UNCHECKED_VALUE

        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        cc = self._compute_correlation_fft(img_1, img_2, padding_mode, high_pass=high_pass, low_pass=low_pass)
        img_shape = img_2.shape
        cc_vs = np.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
        cc_hs = np.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

        (f_vals, fv, fh) = self.extract_peak_region_2d(cc, peak_radius=peak_fit_radius, cc_vs=cc_vs, cc_hs=cc_hs)
        fitted_shifts_vh = self.refine_max_position_2d(f_vals, fv, fh)

        return fitted_shifts_vh[-1] / 2.0


class CenterOfRotationSlidingWindow(CenterOfRotation):
    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side,
        window_width=None,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Semi-automatically find the Center of Rotation (CoR), given two images
        or sinograms. Suitable for half-aquisition scan.

        This method finds the half-shift between two opposite images,  by
        minimizing difference over a moving window.

        The output of this function, allows to compute motor movements for
        aligning the sample rotation axis. Given the following values:

        - L1: distance from source to motor
        - L2: distance from source to detector
        - ps: physical pixel size
        - v: output of this function

        displacement of motor = (L1 / L2 * ps) * v

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        side: string
            Expected region of the CoR. Allowed values: 'left', 'center' or 'right'.
        window_width: int, optional
            Width of window that will slide on the other image / part of the
            sinogram. Default is None.
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`

        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        float
            Estimated center of rotation position from the center of the RoI in pixels.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... CoR_calc = CenterOfRotationSlidingWindow()
        ... cor_position = CoR_calc.find_shift(radio1, radio2)

        Or for noisy images:

        >>> cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))
        """
        if side is None:
            raise ValueError("Side should be one of 'left', 'right', or 'center'. 'None' was given instead")

        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            logging.getLogger(__name__).warning(
                "Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius
            )
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(
            img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_2 = self._prepare_image(
            img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_shape = img_2.shape

        if window_width is None:
            if side.lower() == "center":
                window_width = round(img_shape[-1] / 4.0 * 3.0)
            else:
                window_width = round(img_shape[-1] / 10)
        window_shift = window_width // 2
        window_width = window_shift * 2 + 1

        if side.lower() == "right":
            win_2_start = 0
        elif side.lower() == "left":
            win_2_start = img_shape[-1] - window_width
        elif side.lower() == "center":
            win_2_start = img_shape[-1] // 2 - window_shift
        else:
            raise ValueError("Side should be one of 'left', 'right', or 'center'. '%s' was given instead" % side.lower())

        win_2_end = win_2_start + window_width

        # number of pixels where the window will "slide".
        n = img_shape[-1] - window_width
        diffs_mean = np.empty((n,), dtype=img_1.dtype)
        diffs_std = np.empty((n,), dtype=img_1.dtype)

        for ii in progress_bar(range(n), verbose=self.verbose):
            win_1_start, win_1_end = ii, ii + window_width
            img_diff = img_1[:, win_1_start:win_1_end] - img_2[:, win_2_start:win_2_end]
            diffs_abs = np.abs(img_diff)
            diffs_mean[ii] = diffs_abs.mean()
            diffs_std[ii] = diffs_abs.std()

        diffs_mean = diffs_mean.min() - diffs_mean
        win_ind_max = np.argmax(diffs_mean)

        diffs_std = diffs_std.min() - diffs_std
        if not win_ind_max == np.argmax(diffs_std):
            self.logger.warning(
                "Minimum mean difference and minimum std-dev of differences do not coincide. "
                + "This means that the validity of the found solution might be questionable."
            )

        (f_vals, f_pos) = self.extract_peak_regions_1d(diffs_mean, peak_radius=peak_fit_radius)
        win_pos_max, win_val_max = self.refine_max_position_1d(f_vals, return_vertex_val=True)

        cor_h = -(win_2_start - (win_ind_max + win_pos_max)) / 2.0

        if (side.lower() == "right" and win_ind_max == 0) or (side.lower() == "left" and win_ind_max == n):
            self.logger.warning("Sliding window width %d might be too large!" % window_width)

        if self.verbose:
            cor_pos = -(win_2_start - np.arange(n)) / 2.0

            print("Lowest difference window: index=%d, range=[0, %d]" % (win_ind_max, n))
            print("CoR tested for='%s', found at voxel=%g (from center)" % (side, cor_h))

            f, ax = plt.subplots(1, 1)
            ax.stem(cor_pos, diffs_mean, label="Mean difference")
            ax.stem(cor_h, win_val_max, linefmt="C1-", markerfmt="C1o", label="Best mean difference")
            ax.stem(cor_pos, -diffs_std, linefmt="C2-", markerfmt="C2o", label="Std-dev difference")
            ax.set_title("Window dispersions")
            plt.show(block=False)

        return cor_h


class CenterOfRotationGrowingWindow(CenterOfRotation):
    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side="all",
        min_window_width=11,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Automatically find the Center of Rotation (CoR), given two images or
        sinograms. Suitable for half-aquisition scan.

        This method finds the half-shift between two opposite images,  by
        minimizing difference over a moving window.

        The output of this function, allows to compute motor movements for
        aligning the sample rotation axis. Given the following values:

        - L1: distance from source to motor
        - L2: distance from source to detector
        - ps: physical pixel size
        - v: output of this function

        displacement of motor = (L1 / L2 * ps) * v

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        side: string, optional
            Expected region of the CoR. Allowed values: 'left', 'center', 'right', or 'all'.
            Default is 'all'.
        min_window_width: int, optional
            Minimum window width that covers the common region of the two images /
            sinograms. Default is 11.
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`

        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        float
            Estimated center of rotation position from the center of the RoI in pixels.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... CoR_calc = CenterOfRotationGrowingWindow()
        ... cor_position = CoR_calc.find_shift(radio1, radio2)

        Or for noisy images:

        >>> cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))
        """
        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(
            img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_2 = self._prepare_image(
            img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_shape = img_2.shape

        def window_bounds(mid_point, window_max_width=img_shape[-1]):
            return (
                np.fmax(np.ceil(mid_point - window_max_width / 2), 0).astype(np.int),
                np.fmin(np.ceil(mid_point + window_max_width / 2), img_shape[-1]).astype(np.int),
            )

        img_lower_half_size = np.floor(img_shape[-1] / 2).astype(np.int)
        img_upper_half_size = np.ceil(img_shape[-1] / 2).astype(np.int)

        if side.lower() == "right":
            win_1_mid_start = img_lower_half_size
            win_1_mid_end = np.floor(img_shape[-1] * 3 / 2).astype(np.int) - min_window_width
            win_2_mid_start = -img_upper_half_size + min_window_width
            win_2_mid_end = img_upper_half_size
        elif side.lower() == "left":
            win_1_mid_start = -img_lower_half_size + min_window_width
            win_1_mid_end = img_lower_half_size
            win_2_mid_start = img_upper_half_size
            win_2_mid_end = np.ceil(img_shape[-1] * 3 / 2).astype(np.int) - min_window_width
        elif side.lower() == "center":
            win_1_mid_start = 0
            win_1_mid_end = img_shape[-1]
            win_2_mid_start = 0
            win_2_mid_end = img_shape[-1]
        elif side.lower() == "all":
            win_1_mid_start = -img_lower_half_size + min_window_width
            win_1_mid_end = np.floor(img_shape[-1] * 3 / 2).astype(np.int) - min_window_width
            win_2_mid_start = -img_upper_half_size + min_window_width
            win_2_mid_end = np.ceil(img_shape[-1] * 3 / 2).astype(np.int) - min_window_width
        else:
            raise ValueError("Side should be one of 'left', 'right', or 'center'. '%s' was given instead" % side.lower())

        n1 = win_1_mid_end - win_1_mid_start
        n2 = win_2_mid_end - win_2_mid_start
        # print(n1, n2, window_bounds(win_1_mid_start), window_bounds(win_2_mid_end))

        if not n1 == n2:
            raise ValueError(
                "Internal error: the number of window steps for the two images should be the same."
                + "Found the following configuration instead => Side: %s, #1: %d, #2: %d" % (side, n1, n2)
            )

        diffs_mean = np.empty((n1,), dtype=img_1.dtype)
        diffs_std = np.empty((n1,), dtype=img_1.dtype)

        for ii in progress_bar(range(n1), verbose=self.verbose):
            win_1 = window_bounds(win_1_mid_start + ii)
            win_2 = window_bounds(win_2_mid_end - ii)
            img_diff = img_1[:, win_1[0] : win_1[1]] - img_2[:, win_2[0] : win_2[1]]
            diffs_abs = np.abs(img_diff)
            diffs_mean[ii] = diffs_abs.mean()
            diffs_std[ii] = diffs_abs.std()

        diffs_mean = diffs_mean.min() - diffs_mean
        win_ind_max = np.argmax(diffs_mean)

        diffs_std = diffs_std.min() - diffs_std
        if not win_ind_max == np.argmax(diffs_std):
            self.logger.warning(
                "Minimum mean difference and minimum std-dev of differences do not coincide. "
                + "This means that the validity of the found solution might be questionable."
            )

        (f_vals, f_pos) = self.extract_peak_regions_1d(diffs_mean, peak_radius=peak_fit_radius)
        win_pos_max, win_val_max = self.refine_max_position_1d(f_vals, return_vertex_val=True)

        cor_h = (win_1_mid_start + (win_ind_max + win_pos_max) - img_upper_half_size) / 2.0

        if (side.lower() == "right" and win_ind_max == 0) or (side.lower() == "left" and win_ind_max == n1):
            self.logger.warning("Minimum growing window width %d might be too large!" % min_window_width)

        if self.verbose:
            cor_pos = (win_1_mid_start + np.arange(n1) - img_upper_half_size) / 2.0

            print("Lowest difference window: index=%d, range=[0, %d]" % (win_ind_max, n1))
            print("CoR tested for='%s', found at voxel=%g (from center)" % (side, cor_h))

            f, ax = plt.subplots(1, 1)
            ax.stem(cor_pos, diffs_mean, label="Mean difference")
            ax.stem(cor_h, win_val_max, linefmt="C1-", markerfmt="C1o", label="Best mean difference")
            ax.stem(cor_pos, -diffs_std, linefmt="C2-", markerfmt="C2o", label="Std-dev difference")
            ax.set_title("Window dispersions")
            plt.show(block=False)

        return cor_h


class CenterOfRotationAdaptiveSearch(CenterOfRotation):
    """This adaptive method works by applying a gaussian which highlights, by apodisation, a region
    which can possibly contain the good center of rotation.
    The whole image is spanned during several applications of the apodisation. At each application
    the apodisation function, which is a gaussian, is moved to a new guess position.
    The lenght of the step, by which the gaussian is moved, and its sigma are
    obtained by multiplying the shortest distance from the left or right border with
    a self.step_fraction and  self.sigma_fraction factors which ensure global overlapping.
    for each step a region around the CoR  of each image is selected, and the regions of the two images
    are compared to  calculate a cost function. The value of the cost function, at its minimum
    is used to select the best step at which the CoR is taken as final result.
    The option filtered_cost= True (default) triggers the filtering (according to low_pass and high_pass)
    of the two images which are used for he cost function. ( Note: the low_pass and high_pass options
    are used, if given, also without the filtered_cost option, by being passed to the base class
    CenterOfRotation )
    """

    sigma_fraction = 1.0 / 4.0
    step_fraction = 1.0 / 6.0

    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        high_pass=None,
        low_pass=None,
        margins=None,
        filtered_cost=True,
    ):
        """Find the Center of Rotation (CoR), given two images.

        This method finds the half-shift between two opposite images, by
        means of correlation computed in Fourier space.
        A global search is done on on the detector span (minus a margin) without assuming centered scan conditions.

        The output of this function, allows to compute motor movements for
        aligning the sample rotation axis. Given the following values:

        - L1: distance from source to motor
        - L2: distance from source to detector
        - ps: physical pixel size
        - v: output of this function

        displacement of motor = (L1 / L2 * ps) * v

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        low_pass: float or sequence of two floats.
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`.
        margins:  None or a couple of floats or ints
            if margins is None or in the form of  (margin1,margin2) the search is done between margin1 and  dim_x-1-margin2.
            If left to None then by default (margin1,margin2)  = ( 10, 10 ).
        filtered_cost: boolean.
            True by default. It triggers the use of filtered images in the calculation of the cost function.

        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        float
            Estimated center of rotation position from the center of the RoI in pixels.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... CoR_calc = CenterOfRotationAdaptiveSearch()
        ... cor_position = CoR_calc.find_shift(radio1, radio2)

        Or for noisy images:

        >>> cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3), high_pass=20, low_pass=1   )
        """
        self._check_img_pair_sizes(img_1, img_2)

        used_type = img_1.dtype

        roi_yxhw = self._determine_roi(img_1.shape, roi_yxhw)

        if filtered_cost and (low_pass is not None or high_pass is not None):
            img_filter = fourier_filters.get_bandpass_filter(
                img_1.shape[-2:],
                cutoff_lowpass=low_pass,
                cutoff_highpass=high_pass,
                use_rfft=__have_scipy__,
                data_type=self.data_type,
            )
            # fft2 and iff2 use axes=(-2, -1) by default
            img_filtered_1 = local_ifftn(local_fftn(img_1, axes=(-2, -1)) * img_filter, axes=(-2, -1)).real
            img_filtered_2 = local_ifftn(local_fftn(img_2, axes=(-2, -1)) * img_filter, axes=(-2, -1)).real
        else:
            img_filtered_1 = img_1
            img_filtered_2 = img_2

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        img_filtered_1 = self._prepare_image(img_filtered_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_filtered_2 = self._prepare_image(img_filtered_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        dim_radio = img_1.shape[1]

        if margins is None:
            lim_1, lim_2 = 10, dim_radio - 1 - 10
        else:
            lim_1, lim_2 = margins
            lim_2 = dim_radio - 1 - lim_2

        if lim_1 < 1:
            lim_1 = 1
        if lim_2 > dim_radio - 2:
            lim_2 = dim_radio - 2

        if lim_2 <= lim_1:
            message = (
                "Image shape or cropped selection too small for global search."
                + " After removal of the margins the search limits collide."
                + " The cropped size is %d\n" % (dim_radio)
            )
            raise ValueError(message)

        found_centers = []
        x_cor = lim_1
        while x_cor < lim_2:

            tmp_sigma = min((img_1.shape[1] - x_cor), (x_cor),) * self.sigma_fraction

            tmp_x = (np.arange(img_1.shape[1]) - x_cor) / tmp_sigma
            apodis = np.exp(-tmp_x * tmp_x / 2.0)

            x_cor_rel = x_cor - (img_1.shape[1] // 2)

            img_1_apodised = img_1 * apodis

            try:
                cor_position = super(self.__class__, self).find_shift(
                    img_1_apodised.astype(used_type),
                    img_2.astype(used_type),
                    low_pass=low_pass,
                    high_pass=high_pass,
                    roi_yxhw=roi_yxhw,
                )
            except ValueError as err:
                message = "ValueError from base class {base_class}.find_shift in {my_class}.find_shift  : {err}".format(
                    base_class=super(self.__class__, self).__class__.__name__, my_class=self.__class__.__name__, err=err
                )
                self.logger.warning(message)
                x_cor = min(x_cor + x_cor * self.step_fraction, x_cor + (dim_radio - x_cor) * self.step_fraction)
                continue
            except:
                message = "Unexpected error from base class {base_class}.find_shift in {my_class}.find_shift  : {err}".format(
                    base_class=super(self.__class__, self).__name__, my_class=self.__class__.__name__, err=err
                )
                self.logger.error(message)
                raise

            p_1 = cor_position * 2
            if cor_position < 0:
                p_2 = img_2.shape[1] + cor_position * 2
            else:
                p_2 = -img_2.shape[1] + cor_position * 2

            if abs(x_cor_rel - p_1 / 2) < abs(x_cor_rel - p_2 / 2):
                cor_position = p_1 / 2
            else:
                cor_position = p_2 / 2

            cor_in_img = img_1.shape[1] // 2 + cor_position
            tmp_sigma = min((img_1.shape[1] - cor_in_img), (cor_in_img),) * self.sigma_fraction

            M1 = int(round(cor_position + img_1.shape[1] // 2)) - int(round(tmp_sigma))
            M2 = int(round(cor_position + img_1.shape[1] // 2)) + int(round(tmp_sigma))

            piece_1 = img_filtered_1[:, M1:M2]
            piece_2 = img_filtered_2[:, img_1.shape[1] - M2 : img_1.shape[1] - M1]

            if piece_1.size and piece_2.size:
                piece_1 = piece_1 - piece_1.mean()
                piece_2 = piece_2 - piece_2.mean()
                energy = np.array(piece_1 * piece_1 + piece_2 * piece_2, "d").sum()
                diff_energy = np.array((piece_1 - piece_2) * (piece_1 - piece_2), "d").sum()
                cost = diff_energy / energy

                if not np.isnan(cost):
                    if tmp_sigma * 2 > abs(x_cor_rel - cor_position):
                        found_centers.append([cost, abs(x_cor_rel - cor_position), cor_position, energy])

            x_cor = min(x_cor + x_cor * self.step_fraction, x_cor + (dim_radio - x_cor) * self.step_fraction)

        if len(found_centers) == 0:
            message = "Unable to find any valid CoR candidate in {my_class}.find_shift ".format(
                my_class=self.__class__.__name__
            )
            raise ValueError(message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Now build the neigborhood of the minimum as a list of five elements:
        # the minimum in the middle of the two before, and the two after

        filtered_found_centers = []
        for i in range(len(found_centers)):
            if i > 0:
                if abs(found_centers[i][2] - found_centers[i - 1][2]) < 0.5:
                    filtered_found_centers.append(found_centers[i])
                    continue
            if i + 1 < len(found_centers):
                if abs(found_centers[i][2] - found_centers[i + 1][2]) < 0.5:
                    filtered_found_centers.append(found_centers[i])
                    continue

        if len(filtered_found_centers):
            found_centers = filtered_found_centers

        min_choice = min(found_centers)
        index_min_choice = found_centers.index(min_choice)
        min_neighborood = [
            found_centers[i][2] if (i >= 0 and i < len(found_centers)) else math.nan
            for i in range(index_min_choice - 2, index_min_choice + 2 + 1)
        ]

        score_right = 0
        for i_pos in [3, 4]:
            if abs(min_neighborood[i_pos] - min_neighborood[2]) < 0.5:
                score_right += 1
            else:
                break

        score_left = 0
        for i_pos in [1, 0]:
            if abs(min_neighborood[i_pos] - min_neighborood[2]) < 0.5:
                score_left += 1
            else:
                break

        if score_left + score_right >= 2:
            self.check_result = VALID_VALUE
        else:
            self.check_result = INVALID_VALUE

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # An informative message in case one wish to look at how it has gone
        informative_message = " ".join(
            ["CenterOfRotationAdaptiveSearch found this neighborood of the optimal position:"]
            + [str(t) if not math.isnan(t) else "N.A." for t in min_neighborood]
        )
        self.logger.debug(informative_message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # The return value is the optimum which had been placed in the middle of the neighborood
        cor_position = min_neighborood[2]
        return cor_position

    __call__ = find_shift


class DetectorTranslationAlongBeam(AlignmentBase):
    def find_shift(
        self,
        img_stack: np.ndarray,
        img_pos: np.array,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
        return_shifts=False,
        use_adjacent_imgs=False,
    ):
        """Find the vertical and horizontal shifts for translations of the
        detector along the beam direction.

        These shifts are in pixels-per-unit-translation, and they are due to
        the misalignment of the translation stage, with respect to the beam
        propagation direction.

        To compute the vertical and horizontal tilt angles from the obtained `shift_pix`:

        >>> tilt_deg = np.rad2deg(np.arctan(shift_pix * pixel_size))

        where `pixel_size` and and the input parameter `img_pos` have to be
        expressed in the same units.

        Parameters
        ----------
        img_stack: numpy.ndarray
            A stack of images (usually 4) at different distances
        img_pos: numpy.ndarray
            Position of the images along the translation axis
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`.
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`.
        return_shifts: boolean, optional
            Adds a third returned argument, containing the pixel shifts of each
            image with respect to the first one in the stack. Defaults to False.
        use_adjacent_imgs: boolean, optional
            Compute correlation between adjacent images.
            It can be used when dealing with large shifts, to avoid overflowing the shift.
            This option allows to replicate the behavior of the reference function `alignxc.m`
            However, it is detrimental to shift fitting accuracy. Defaults to False.

        Returns
        -------
        coeff_v: float
            Estimated vertical shift in pixel per unit-distance of the detector translation.
        coeff_h: float
            Estimated horizontal shift in pixel per unit-distance of the detector translation.
        shifts_vh: list, optional
            The pixel shifts of each image with respect to the first image in the stack.
            Activated if return_shifts is True.

        Examples
        --------
        The following example creates a stack of shifted images, and retrieves the computed shift.
        Here we use a high-pass filter, due to the presence of some low-frequency noise component.

        >>> import numpy as np
        ... import scipy as sp
        ... import scipy.ndimage
        ... from nabu.preproc.alignment import  DetectorTranslationAlongBeam
        ...
        ... tr_calc = DetectorTranslationAlongBeam()
        ...
        ... stack = np.zeros([4, 512, 512])
        ...
        ... # Add low frequency spurious component
        ... for i in range(4):
        ...     stack[i, 200 - i * 10, 200 - i * 10] = 1
        ... stack = sp.ndimage.filters.gaussian_filter(stack, [0, 10, 10.0]) * 100
        ...
        ... # Add the feature
        ... x, y = np.meshgrid(np.arange(stack.shape[-1]), np.arange(stack.shape[-2]))
        ... for i in range(4):
        ...     xc = x - (250 + i * 1.234)
        ...     yc = y - (250 + i * 1.234 * 2)
        ...     stack[i] += np.exp(-(xc * xc + yc * yc) * 0.5)
        ...
        ... # Image translation along the beam
        ... img_pos = np.arange(4)
        ...
        ... # Find the shifts from the features
        ... shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos, high_pass=1.0)
        ... print(shifts_v, shifts_h)
        >>> ( -2.47 , -1.236 )

        and the following commands convert the shifts in angular tilts:

        >>> tilt_v_deg = np.rad2deg(np.arctan(shifts_v * pixel_size))
        >>> tilt_h_deg = np.rad2deg(np.arctan(shifts_h * pixel_size))

        To enable the legacy behavior of `alignxc.m` (correlation between adjacent images):

        >>> shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos, use_adjacent_imgs=True)

        To plot the correlation shifts and the fitted straight lines for both directions:

        >>> tr_calc = DetectorTranslationAlongBeam(verbose=True)
        ... shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos)
        """
        self._check_img_stack_size(img_stack, img_pos)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        num_imgs = img_stack.shape[0]
        img_shape = img_stack.shape[-2:]
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_stack = self._prepare_image(img_stack, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        # do correlations
        ccs = [
            self._compute_correlation_fft(
                img_stack[ii - 1 if use_adjacent_imgs else 0, ...],
                img_stack[ii, ...],
                padding_mode,
                high_pass=high_pass,
                low_pass=low_pass,
            )
            for ii in range(1, num_imgs)
        ]

        img_shape = img_stack.shape[-2:]
        cc_vs = np.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
        cc_hs = np.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

        shifts_vh = np.empty((num_imgs, 2))
        for ii, cc in enumerate(ccs):
            (f_vals, fv, fh) = self.extract_peak_region_2d(cc, peak_radius=peak_fit_radius, cc_vs=cc_vs, cc_hs=cc_hs)
            shifts_vh[ii + 1, :] = self.refine_max_position_2d(f_vals, fv, fh)

        if use_adjacent_imgs:
            shifts_vh = np.cumsum(shifts_vh, axis=0)

        # Polynomial.fit is supposed to be more numerically stable than polyfit
        # (according to numpy)
        coeffs_v = Polynomial.fit(img_pos, shifts_vh[:, 0], deg=1).convert().coef
        coeffs_h = Polynomial.fit(img_pos, shifts_vh[:, 1], deg=1).convert().coef

        if self.verbose:
            print("Fitted pixel shifts per unit-length: vertical = %f, horizontal = %f" % (coeffs_v[1], coeffs_h[1]))
            f, axs = plt.subplots(1, 2)
            axs[0].scatter(img_pos, shifts_vh[:, 0])
            axs[0].plot(img_pos, polyval(img_pos, coeffs_v), "-C1")
            axs[0].set_title("Vertical shifts")
            axs[1].scatter(img_pos, shifts_vh[:, 1])
            axs[1].plot(img_pos, polyval(img_pos, coeffs_h), "-C1")
            axs[1].set_title("Horizontal shifts")
            plt.show(block=False)

        if return_shifts:
            return coeffs_v[1], coeffs_h[1], shifts_vh
        else:
            return coeffs_v[1], coeffs_h[1]


class CameraTilt(CenterOfRotation):
    def compute_angle(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Find the camera tilt, given two opposite images.

        This method finds the tilt between the camera pixel columns and the
        rotation axis, by performing a 1-dimensional correlation between two
        opposite images.

        The output of this function, allows to compute motor movements for
        aligning the camera tilt.

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`

        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        cor_offset_pix: float
            Estimated center of rotation position from the center of the RoI in pixels.
        tilt_deg: float
            Estimated camera tilt angle in degrees.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... tilt_calc = CameraTilt()
        ... cor_offset, camera_tilt = tilt_calc.compute_angle(radio1, radio2)

        Or for noisy images:

        >>> cor_offset, camera_tilt = tilt_calc.compute_angle(radio1, radio2, median_filt_shape=(3, 3))
        """
        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        cc = self._compute_correlation_fft(img_1, img_2, padding_mode, axes=(-1,), high_pass=high_pass, low_pass=low_pass,)

        img_shape = img_2.shape
        cc_h_coords = np.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

        (f_vals, fh) = self.extract_peak_regions_1d(cc, peak_radius=peak_fit_radius, cc_coords=cc_h_coords)
        fitted_shifts_h = self.refine_max_position_1d(f_vals)
        fitted_shifts_h += fh[1, :]

        # Computing tilt
        if __have_scipy__:
            fitted_shifts_h = median_filter(fitted_shifts_h, size=3)
        else:
            fitted_shifts_h = median_filter_1d(fitted_shifts_h, kernel_size=3)

        half_img_size = (img_shape[-2] - 1) / 2
        cc_v_coords = np.linspace(-half_img_size, half_img_size, img_shape[-2])
        coeffs_h = Polynomial.fit(cc_v_coords, fitted_shifts_h, deg=1).convert().coef

        tilt_deg = np.rad2deg(-coeffs_h[1] / 2)
        cor_offset_pix = coeffs_h[0] / 2

        if self.verbose:
            print(
                "Fitted center of rotation (pixels):", cor_offset_pix, "and camera tilt (degrees):", tilt_deg,
            )
            f, ax = plt.subplots(1, 1)
            ax.scatter(cc_v_coords, fitted_shifts_h)
            ax.plot(cc_v_coords, polyval(cc_v_coords, coeffs_h), "-C1")
            ax.set_title("Correlation peaks")
            plt.show(block=False)

        return cor_offset_pix, tilt_deg


class CameraFocus(CenterOfRotation):
    def find_distance(
        self,
        img_stack: np.ndarray,
        img_pos: np.array,
        metric="std",
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Find the focal distance of the camera system.

        This routine computes the motor position that corresponds to having the
        scintillator on the focal plain of the camera system.

        Parameters
        ----------
        img_stack: numpy.ndarray
            A stack of images at different distances.
        img_pos: numpy.ndarray
            Position of the images along the translation axis
        metric: string, optional
            The property, whose maximize occurs at the focal position.
            Defaults to 'std' (standard deviation).
            All options are: 'std' | 'grad' | 'psd'
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`.
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`.

        Returns
        -------
        focus_pos: float
            Estimated position of the focal plane of the camera system.
        focus_ind: float
            Image index of the estimated position of the focal plane of the camera system (starting from 1!).

        Examples
        --------
        Given the focal stack associated to multiple positions of the camera
        focus motor called `img_stack`, and the associated positions `img_pos`,
        the following code computes the highest focus position:

        >>> focus_calc = alignment.CameraFocus()
        ... focus_pos, focus_ind = focus_calc.find_distance(img_stack, img_pos)

        where `focus_pos` is the corresponding motor position, and `focus_ind`
        is the associated image position (starting from 1).
        """
        self._check_img_stack_size(img_stack, img_pos)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        num_imgs = img_stack.shape[0]
        img_shape = img_stack.shape[-2:]
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_stack = self._prepare_image(
            img_stack, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, low_pass=low_pass, high_pass=high_pass,
        )

        img_stds = np.std(img_stack, axis=(-2, -1)) / np.mean(img_stack, axis=(-2, -1))

        # assuming images are equispaced
        focus_step = (img_pos[-1] - img_pos[0]) / (num_imgs - 1)

        img_inds = np.arange(num_imgs)
        (f_vals, f_pos) = self.extract_peak_regions_1d(img_stds, peak_radius=peak_fit_radius, cc_coords=img_inds)
        focus_ind, img_std_max = self.refine_max_position_1d(f_vals, return_vertex_val=True)
        focus_ind += f_pos[1, :]

        focus_pos = img_pos[0] + focus_step * focus_ind
        focus_ind += 1

        if self.verbose:
            print(
                "Fitted focus motor position:", focus_pos, "and corresponding image position:", focus_ind,
            )
            f, ax = plt.subplots(1, 1)
            ax.stem(img_pos, img_stds)
            ax.stem(focus_pos, img_std_max, linefmt="C1-", markerfmt="C1o")
            ax.set_title("Images std")
            plt.show(block=False)

        return focus_pos, focus_ind

    def _check_img_block_size(self, img_shape, regions_number, suggest_new_shape=True):
        img_shape = np.array(img_shape)
        new_shape = img_shape
        if not len(img_shape) == 2:
            raise ValueError(
                "Images need to be square 2-dimensional and with shape multiple of the number of assigned regions.\n"
                " Image shape: %s, regions number: %d" % (img_shape, regions_number)
            )
        if not (img_shape[0] == img_shape[1] and np.all((np.array(img_shape) % regions_number) == 0)):
            new_shape = (img_shape // regions_number) * regions_number
            new_shape = np.fmin(new_shape, new_shape.min())
            message = (
                "Images need to be square 2-dimensional and with shape multiple of the number of assigned regions.\n"
                " Image shape: %s, regions number: %d. Cropping to image shape: %s" % (img_shape, regions_number, new_shape)
            )
            if suggest_new_shape:
                print(message)
            else:
                raise ValueError(message)
        return new_shape

    @staticmethod
    def _fit_plane(f_vals):
        f_vals_half_shape = (np.array(f_vals.shape) - 1) / 2

        fy = np.linspace(-f_vals_half_shape[-2], f_vals_half_shape[-2], f_vals.shape[-2])
        fx = np.linspace(-f_vals_half_shape[-1], f_vals_half_shape[-1], f_vals.shape[-1])

        fy, fx = np.meshgrid(fy, fx, indexing="ij")
        coords = np.array([np.ones(f_vals.size), fy.flatten(), fx.flatten()])

        return np.linalg.lstsq(coords.T, f_vals.flatten(), rcond=None)[0], fy, fx

    def find_scintillator_tilt(
        self,
        img_stack: np.ndarray,
        img_pos: np.array,
        regions_number=4,
        metric="std",
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
    ):
        """Finds the scintillator tilt and focal distance of the camera system.

        This routine computes the mounting tilt of the scintillator and the
        motor position that corresponds to having the scintillator on the focal
        plain of the camera system.

        The input is supposed to be a stack of square images, whose sizes are
        multiples of the `regions_number` parameter. If images with a different
        size are passed, this function will crop the images. This also generates
        a warning. To suppress the warning, it is suggested to specify a ROI
        that satisfies those criteria (see examples).

        The computed tilts `tilt_vh` are in unit-length per pixel-size. To
        obtain the tilts it is necessary to divide by the pixel-size:

        >>> tilt_vh_deg = np.rad2deg(np.arctan(tilt_vh / pixel_size))

        The correction to be applied is:

        >>> tilt_corr_vh_deg = - np.rad2deg(np.arctan(tilt_vh / pixel_size))

        The legacy octave macros computed the approximation of these values in radians:

        >>> tilt_corr_vh_rad = - tilt_vh / pixel_size

        Note that `pixel_size` should be in the same unit scale as `img_pos`.

        Parameters
        ----------
        img_stack: numpy.ndarray
            A stack of images at different distances.
        img_pos: numpy.ndarray
            Position of the images along the translation axis
        regions_number: int, optional
            The number of regions to subdivide the image into, along each direction.
            Defaults to 4.
        metric: string, optional
            The property, whose maximize occurs at the focal position.
            Defaults to 'std' (standard deviation).
            All options are: 'std' | 'grad' | 'psd'
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> auto-suggest correct size.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`.
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`.

        Returns
        -------
        focus_pos: float
            Estimated position of the focal plane of the camera system.
        focus_ind: float
            Image index of the estimated position of the focal plane of the
            camera system (starting from 1!).
        tilts_vh: tuple(float, float)
            Estimated scintillator tilts in the vertical and horizontal
            direction respectively per unit-length per pixel-size.

        Examples
        --------
        Given the focal stack associated to multiple positions of the camera
        focus motor called `img_stack`, and the associated positions `img_pos`,
        the following code computes the highest focus position:

        >>> focus_calc = alignment.CameraFocus()
        ... focus_pos, focus_ind, tilts_vh = focus_calc.find_scintillator_tilt(img_stack, img_pos)
        ... tilt_corr_vh_deg = - np.rad2deg(np.arctan(tilt_vh / pixel_size))

        or to keep compatibility with the old octave macros:

        >>> tilt_corr_vh_rad = - tilt_vh / pixel_size

        For non square images, or images with sizes that are not multiples of
        the `regions_number` parameter, and no ROI is being passed, this function
        will try to crop the image stack to the correct size.
        If you want to remove the warning message, it is suggested to set a ROI
        like the following:

        >>> regions_number = 4
        ... img_roi = (np.array(img_stack.shape[1:]) // regions_number) * regions_number
        ... img_roi = np.fmin(img_roi, img_roi.min())
        ... focus_calc = alignment.CameraFocus()
        ... focus_pos, focus_ind, tilts_vh = focus_calc.find_scintillator_tilt(
        ...     img_stack, img_pos, roi_yxhw=img_roi, regions_number=regions_number)
        """
        self._check_img_stack_size(img_stack, img_pos)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        num_imgs = img_stack.shape[0]
        img_shape = img_stack.shape[-2:]
        if roi_yxhw is None:
            # If no roi is being passed, we try to crop the images to the
            # correct size, if needed
            roi_yxhw = self._check_img_block_size(img_shape, regions_number, suggest_new_shape=True)
            roi_yxhw = self._determine_roi(img_shape, roi_yxhw)
        else:
            # If a roi is being passed, and the images don't have the correct
            # shape, we raise an error
            roi_yxhw = self._determine_roi(img_shape, roi_yxhw)
            self._check_img_block_size(roi_yxhw[2:], regions_number, suggest_new_shape=False)

        img_stack = self._prepare_image(
            img_stack, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, low_pass=low_pass, high_pass=high_pass,
        )
        img_shape = img_stack.shape[-2:]

        block_size = np.array(img_shape) / regions_number
        block_stack_size = np.array([num_imgs, regions_number, block_size[-2], regions_number, block_size[-1]], dtype=np.int,)
        img_stack = np.reshape(img_stack, block_stack_size)

        img_stds = np.std(img_stack, axis=(-3, -1)) / np.mean(img_stack, axis=(-3, -1))
        img_stds = np.reshape(img_stds, [num_imgs, -1]).transpose()

        # assuming images are equispaced
        focus_step = (img_pos[-1] - img_pos[0]) / (num_imgs - 1)

        img_inds = np.arange(num_imgs)
        (f_vals, f_pos) = self.extract_peak_regions_1d(img_stds, peak_radius=peak_fit_radius, cc_coords=img_inds)
        focus_inds = self.refine_max_position_1d(f_vals)
        focus_inds += f_pos[1, :]

        focus_poss = img_pos[0] + focus_step * focus_inds

        # Fitting the plane
        focus_poss = np.reshape(focus_poss, [regions_number, regions_number])
        coeffs, fy, fx = self._fit_plane(focus_poss)
        focus_pos, tg_v, tg_h = coeffs

        # The angular coefficient along x is the tilt around the y axis and vice-versa
        tilts_vh = np.array([tg_h, tg_v]) / block_size

        focus_ind = np.mean(focus_inds) + 1

        if self.verbose:
            print(
                "Fitted focus motor position:", focus_pos, "and corresponding image position:", focus_ind,
            )
            print("Fitted tilts (to be divided by pixel size, and converted to deg): (v, h) %s" % tilts_vh)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.plot_wireframe(fx, fy, focus_poss)
            regions_half_shape = (regions_number - 1) / 2
            base_points = np.linspace(-regions_half_shape, regions_half_shape, regions_number)
            ax.plot(
                np.zeros((regions_number,)), base_points, np.polyval([tg_v, focus_pos], base_points), "C2",
            )
            ax.plot(
                base_points, np.zeros((regions_number,)), np.polyval([tg_h, focus_pos], base_points), "C2",
            )
            ax.scatter(0, 0, focus_pos, marker="o", c="C1")
            ax.set_title("Images std")
            plt.show(block=False)

        return focus_pos, focus_ind, tilts_vh
