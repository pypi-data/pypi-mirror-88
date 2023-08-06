import numpy as np
import pycuda.gpuarray as garray
from .sinogram import SinoProcessing, SinoNormalization
from ..cuda.processing import CudaProcessing
from ..cuda.kernel import CudaKernel
from ..utils import get_cuda_srcfile, updiv


class CudaSinoProcessing(SinoProcessing, CudaProcessing):
    def __init__(self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False, cuda_options=None):
        """
        Initialize a CudaSinoProcessing instance.
        Please see the documentation of nabu.preproc.sinogram.SinoProcessing
        and nabu.cuda.processing.CudaProcessing.
        """
        SinoProcessing.__init__(
            self, sinos_shape=sinos_shape, radios_shape=radios_shape, rot_center=rot_center,
            halftomo=halftomo,
        )
        if cuda_options is None:
            cuda_options = {}
        CudaProcessing.__init__(self, **cuda_options)
        self._init_cuda_halftomo()


    def _init_cuda_halftomo(self):
        if not(self.halftomo):
            return
        self.halftomo_kernel = CudaKernel(
            "halftomo_kernel",
            get_cuda_srcfile("halftomo.cu"),
            signature="PPPiii",
        )
        rc = self._rot_center_int
        blk = (32, 32, 1) # tune ?
        self._halftomo_blksize = blk
        self._halftomo_gridsize = (
            updiv(2 * rc, blk[0]),
            updiv(self.n_angles//2, blk[1]),
            1
        )
        d = self.n_x - rc # will have to be adapted for varying axis pos
        self.halftomo_weights = np.linspace(0, 1, d, endpoint=True, dtype="f")
        self.d_halftomo_weights = garray.to_gpu(self.halftomo_weights)
        if self._halftomo_flip:
            self.xflip_kernel = CudaKernel(
                "reverse2D_x",
                get_cuda_srcfile("ElementOp.cu"),
                signature="Pii"
            )
            blk = (32, 32, 1)
            self._xflip_blksize = blk
            self._xflip_gridsize_1 = (
                updiv(self.n_x, blk[0]),
                updiv(self.n_angles, blk[1]),
                1
            )
            self._xflip_gridsize_2 = self._halftomo_gridsize


    # Overwrite parent method
    def _radios_to_sinos_simple(self, radios, output, copy=False):
        if not(copy) and output is None:
            return radios.transpose(axes=(1, 0, 2)) # view
        if output is None: # copy and output is None
            na, nz, nx = radios.shape
            output = garray.zeros((nz, na, nx), "f")
        # not(copy) and output is not None
        for i in range(output.shape[0]):
            output[i, :, :] = radios[:, i, :]
        return output



    # Overwrite parent method
    def _radios_to_sinos_halftomo(self, radios, sinos):
        # TODO
        if not(np.isscalar(self.rot_center)):
            raise NotImplementedError("Half tomo with varying rotation axis position is not implemented yet")
        #

        n_a, n_z, n_x = radios.shape
        n_a2 = n_a // 2
        rc = self._rot_center_int
        out_dwidth = 2 * rc
        if sinos is not None:
            if sinos.shape[-1] != out_dwidth:
                raise ValueError(
                    "Expected sinos sinogram last dimension to have %d elements"
                    % out_dwidth
                )
            if sinos.shape[-2] != n_a2:
                raise ValueError("Expected sinograms to have %d angles" % n_a2)
        else:
            sinos = garray.zeros(self.sinos_halftomo_shape, dtype=np.float32)

        # need to use a contiguous 2D, array otherwise kernel does not work
        d_radio = radios[:, 0, :].copy()
        for i in range(n_z):
            d_radio[:] = radios[:, i, :].copy()
            if self._halftomo_flip:
                self.xflip_kernel(
                    d_radio, n_x, n_a,
                    grid=self._xflip_gridsize_1, block=self._xflip_blksize
                )
            self.halftomo_kernel(
                d_radio,
                sinos[i],
                self.d_halftomo_weights,
                n_a, n_x, rc,
                grid=self._halftomo_gridsize,
                block=self._halftomo_blksize
            )
            if self._halftomo_flip:
                self.xflip_kernel(
                    sinos[i], 2*rc, n_a2,
                    grid=self._xflip_gridsize_2, block=self._xflip_blksize
                )
        return sinos


class CudaSinoNormalization(SinoNormalization, CudaProcessing):
    def __init__(self, kind="chebyshev", sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False, cuda_options=None):
        SinoNormalization.__init__(
            self, kind=kind, sinos_shape=sinos_shape, radios_shape=radios_shape,
            rot_center=rot_center, halftomo=halftomo,
        )
        if cuda_options is None:
            cuda_options = {}
        CudaProcessing.__init__(self, **cuda_options)
        self._init_cuda_normalization()


    def _init_cuda_normalization(self):
        self._cuda_kernel = CudaKernel(
            self._get_norm_func_name(),
            filename=get_cuda_srcfile("normalization.cu"),
            signature="Piii",
        )
        self._cuda_kernel_args = [
            np.int32(self.n_x), np.int32(self.n_angles), np.int32(self.n_z)
        ]
        blk = (1, 64, 16) # TODO tune ?
        self._cuda_kernel_kwargs = {
            "block": blk,
            "grid": (1, int(updiv(self.n_angles, blk[1])), int(updiv(self.n_z, blk[2]))),
        }


    def normalize(self, sino):
        self._cuda_kernel(
            sino, *self._cuda_kernel_args, **self._cuda_kernel_kwargs
        )
        return sino
