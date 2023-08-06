import numpy as np
import pytest
from nabu.utils import clip_circle
from nabu.testutils import get_data, compare_arrays
from nabu.preproc.rings import Deringer
from nabu.thirdparty.pore3d_deringer_munch import  munchetal_filter
from nabu.cuda.utils import __has_pycuda__
__have_gpuderinger__ = False
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.preproc.rings_cuda import CudaMunchDeringer, __have_pypwt__, __have_skcuda__
    if __have_pypwt__ and __have_skcuda__:
        __have_gpuderinger__ = True


@pytest.fixture(scope='class')
def bootstrap(request):
    cls = request.cls
    cls.sino = get_data("mri_sino500.npz")["data"]
    cls.tol = 5e-3
    cls.rings = {
        150: 0.5,
        -150: 0.5
    }
    cls.fw_levels = 4
    cls.fw_sigma = 1.
    cls.fw_wname = "db5"


@pytest.mark.usefixtures('bootstrap')
class TestDeringer:

    @staticmethod
    def add_stripes_to_sino(sino, rings_desc):
        """
        Create a new sinogram by adding synthetic stripes to an existing one.

        Parameters
        ----------
        sino: array-like
            Sinogram.
        rings_desc: dict
            Dictionary describing the stripes locations and intensity.
            The location is an integer in [0, N[ where N is the number of columns.
            The intensity is a float: percentage of the current column mean value.
        """
        sino_out = np.copy(sino)
        for loc, intensity in rings_desc.items():
            sino_out[:, loc] += sino[:, loc].mean() * intensity
        return sino_out


    @pytest.mark.skipif(munchetal_filter is None, reason="Need PyWavelets for this test")
    def test_munch_deringer(self):
        deringer = Deringer(
            sinos_shape=self.sino.shape, method="munch",
            deringer_args=[self.fw_levels, self.fw_sigma],
            deringer_kwargs={"wname": self.fw_wname}
        )
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        # Reference destriping with pore3d "munchetal_filter"
        ref = munchetal_filter(sino, self.fw_levels, self.fw_sigma, wname=self.fw_wname)
        # Wrapping with DeRinger
        res = np.zeros((1, ) + sino.shape, dtype=np.float32)
        deringer.correct_rings(sino, output=res)

        err_max = np.max(np.abs(res[0] - ref))

        assert err_max < self.tol, "Max error is too high"


    @pytest.mark.skipif(not(__have_gpuderinger__), reason="Need pycuda, pypwt and scikit-cuda for this test")
    def test_cuda_munch_deringer(self):
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        deringer = CudaMunchDeringer(
            self.fw_levels, self.fw_sigma, wname=self.fw_wname, sinos_shape=self.sino.shape
        )
        d_sino = garray.to_gpu(sino)
        deringer.destripe_munch(d_sino)
        res = d_sino.get()

        ref = munchetal_filter(sino, self.fw_levels, self.fw_sigma, wname=self.fw_wname)

        err_max = np.max(np.abs(res - ref))
        assert err_max < 1e-1, "Max error is too high"


