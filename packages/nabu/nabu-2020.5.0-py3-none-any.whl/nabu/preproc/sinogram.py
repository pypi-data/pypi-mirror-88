import numpy as np
from ..utils import get_2D_3D_shape, check_supported


class SinoProcessing(object):
    """
    A base class for processing sinograms.
    """

    def __init__(self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False):
        """
        Initialize a SinoProcessing instance.

        Parameters
        ----------
        sinos_shape: tuple of int
            Shape of the stack of sinograms, in the form `(n_z, n_angles, n_x)`.
            If not provided, it is derived from `radios_shape`.
        radios_shape: tuple of int
            Shape of the chunk of radios, in the form `(n_angles, n_z, n_x)`.
            If not provided, it is derived from `sinos_shape`.
        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        halftomo: bool
            Whether "half tomography" is enabled. Default is False.
        """
        self._get_shapes(sinos_shape, radios_shape)
        self.halftomo = halftomo
        self.set_rot_center(rot_center)
        self._configure_halftomo()


    def _get_shapes(self, sinos_shape, radios_shape):
        if (sinos_shape is None) and (radios_shape is None):
            raise ValueError("Need to provide sinos_shape and/or radios_shape")
        if sinos_shape is None:
            n_a, n_z, n_x = get_2D_3D_shape(radios_shape)
            sinos_shape = (n_z, n_a, n_x)
        elif len(sinos_shape) == 2:
            sinos_shape = (1, ) + sinos_shape
        if radios_shape is None:
            n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
            radios_shape = (n_a, n_z, n_x)
        elif len(radios_shape) == 2:
            radios_shape = (1, ) + radios_shape

        self.sinos_shape = sinos_shape
        self.radios_shape = radios_shape
        n_a, n_z, n_x = radios_shape
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x


    def set_rot_center(self, rot_center):
        """
        Set the rotation axis position for the current radios/sinos stack.

        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        """
        if rot_center is None:
            rot_center = (self.n_x - 1) / 2.
        if not(np.isscalar(rot_center)):
            rot_center = np.array(rot_center)
            if rot_center.size != self.n_angles:
                raise ValueError(
                    "Expected rot_center to have %d elements but got %d"
                    % (self.n_angles, rot_center.size)
                )
        self.rot_center = rot_center
        self._rot_center_int = int(round(self.rot_center))
        # If CoR is on the left: "flip" the logic
        self._halftomo_flip = False
        if self.halftomo:
            rc = self._rot_center_int
            if rc < (self.n_x - 1)/2:
                rc = self.n_x - 1 - rc
                self._rot_center_int = rc
                self.rot_center = self.n_x - self.rot_center
                self._halftomo_flip = True
        #

    def _configure_halftomo(self):
        if not(self.halftomo):
            return
        assert (self.n_angles % 2) == 0, "Half tomography: expected an even number of angles (got %d)" % self.n_angles
        if abs(self.rot_center - ((self.n_x - 1) / 2.)) < 1: # which tol ?
            raise ValueError(
                "Half tomography: incompatible rotation axis position: %.2f"
                % self.rot_center
            )
        self.sinos_halftomo_shape = (self.n_z, self.n_angles // 2, 2 * self._rot_center_int)


    def _check_array_shape(self, array, kind="radio"):
        expected_shape = self.radios_shape if "radio" in kind else self.sinos_shape
        assert array.shape == expected_shape, "Expected radios shape %s, but got %s" % (expected_shape, array.shape)


    def _radios_to_sinos_simple(self, radios, output, copy=False):
        sinos = np.rollaxis(radios, 1, 0)  # view
        if not(copy) and output is None:
            return sinos
        if output is None: # copy and output is None
            return np.ascontiguousarray(sinos)  # copy
        # not(copy) and output is not None
        for i in range(output.shape[0]):
            output[i] = sinos[i]
        return output


    def _radios_to_sinos_halftomo(self, radios, sinos):
        # TODO
        if not(np.isscalar(self.rot_center)):
            raise NotImplementedError("Half tomo with varying rotation axis position is not implemented yet")
        #

        n_a, n_z, n_x = radios.shape
        n_a2 = n_a // 2
        out_dwidth = 2 * self._rot_center_int
        if sinos is not None:
            if sinos.shape[-1] != out_dwidth:
                raise ValueError(
                    "Expected sinos sinogram last dimension to have %d elements"
                    % out_dwidth
                )
            if sinos.shape[-2] != n_a2:
                raise ValueError("Expected sinograms to have %d angles" % n_a2)
        else:
            sinos = np.zeros(self.sinos_halftomo_shape, dtype=np.float32)
        for i in range(n_z):
            radio = radios[:, i, :]
            if self._halftomo_flip:
                radio = radio[:, ::-1]
            sinos[i][:] = convert_halftomo(radio, self._rot_center_int)
            if self._halftomo_flip:
                sinos[i][:] = sinos[i][:, ::-1]
        return sinos


    @property
    def output_shape(self):
        """
        Get the output sinograms shape.
        """
        if self.halftomo:
            return self.sinos_halftomo_shape
        return self.sinos_shape


    def radios_to_sinos(self, radios, output=None, copy=False):
        """
        Convert a chunk of radios to a stack of sinograms.

        Parameters
        -----------
        radios: array
            Radios to convert
        output: array, optional
            Output sinograms array, pre-allocated
        """
        self._check_array_shape(radios, kind="radio")
        if self.halftomo:
            return self._radios_to_sinos_halftomo(radios, output)
        return self._radios_to_sinos_simple(radios, output, copy=copy)



def convert_halftomo(sino, rotation_axis_position):
    """
    Converts a sinogram into a sinogram with extended FOV with the "half tomography"
    setting.
    """
    assert sino.ndim == 2
    assert (sino.shape[0] % 2) == 0
    na, nx = sino.shape
    na2 = na // 2
    r = rotation_axis_position
    d = nx - r
    res = np.zeros((na2, 2 * r), dtype="f")

    sino1 = sino[:na2, :]
    sino2 = sino[na2:, ::-1]
    res[:, : nx - d] = sino1[:, : nx - d]
    #
    w1 = np.linspace(0, 1, d, endpoint=True)
    res[:, nx - d : nx] = (1 - w1) * sino1[:, nx - d :] + w1 * sino2[:, d : 2 * d]
    #
    res[:, nx:] = sino2[:, 2 * d :]

    return res



class SinoNormalization(SinoProcessing):
    """
    A class for sinogram normalization utilities.
    """

    kinds = [
        "chebyshev"
    ]

    def __init__(self, kind="chebyshev", sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False):
        """
        Initialize a SinoNormalization class.
        Please see the documentation of SinoProcessing for the other parameters.

        Parameters
        -----------
        kind: str, optional
            Normalization type. They can be the following:
               - chebyshev: Each sinogram line is estimated by a Chebyshev polynomial
               of degree 2. This estimation is then subtracted from the sinogram.
            Default is "chebyshev"
        """
        super().__init__(
            sinos_shape=sinos_shape, radios_shape=radios_shape, rot_center=rot_center,
            halftomo=halftomo
        )
        self._set_kind(kind)


    def _set_kind(self, kind):
        check_supported(kind, self.kinds, "sinogram normalization kind")
        self.normalization_kind = kind


    def _normalize_chebyshev_2D(self, sino):
        output = sino # inplace
        Nr, Nc = sino.shape
        J = np.arange(Nc)
        x = 2.* (J + 0.5 - Nc/2)/Nc
        sum0 = Nc
        f2 = (3.0*x*x-1.0)
        sum1 = (x**2).sum()
        sum2 = (f2**2).sum()
        for i in range(Nr):
            ff0 = sino[i, :].sum()
            ff1 = (x * sino[i, :]).sum()
            ff2 = (f2*sino[i, :]).sum()
            output[i, :] = sino[i, :] - (ff0/sum0 + ff1*x/sum1 + ff2*f2/sum2)
        return output


    def _normalize_chebyshev_3D(self, sino):
        for i in range(sino.shape[0]):
            self._normalize_chebyshev_2D(sino[i])
        return sino


    def _normalize_chebyshev(self, sino):
        if sino.ndim == 2:
            res = self._normalize_chebyshev_2D(sino)
        else:
            res = self._normalize_chebyshev_3D(sino)
        return res


    def _get_norm_func_name(self, prefix=""):
        return prefix + "normalize_" + self.normalization_kind


    def normalize(self, sino):
        """
        Normalize a sinogram or stack of sinogram.
        The process is done in-place, meaning that the sinogram content is overwritten.
        """
        norm_func = getattr(self, self._get_norm_func_name(prefix="_"))
        return norm_func(sino)


