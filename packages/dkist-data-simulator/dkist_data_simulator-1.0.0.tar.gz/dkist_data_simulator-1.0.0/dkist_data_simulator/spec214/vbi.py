import numpy as np

import astropy.units as u
from astropy.wcs import WCS

from .core import Spec214Dataset


class BaseVBIDataset(Spec214Dataset):
    """
    A base class for VBI datasets.
    """

    def __init__(self,
                 n_time,
                 time_delta,
                 *,
                 linewave,
                 detector_shape=(4096, 4096)):

        array_shape = list(detector_shape)
        dataset_shape_rev = list(detector_shape) + [n_time]

        super().__init__(dataset_shape_rev[::-1], array_shape, time_delta=time_delta, instrument='vbi')

        self.add_constant_key("DTYPE1", "SPATIAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "TEMPORAL")
        self.add_constant_key("DPNAME1", "spatial x")
        self.add_constant_key("DPNAME2", "spatial y")
        self.add_constant_key("DPNAME3", "frame number")
        self.add_constant_key("DWNAME1", "helioprojective longitude")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DWNAME3", "time")
        self.add_constant_key("DUNIT1", "arcsec")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "s")
        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        self.plate_scale = 0.011 * u.arcsec / u.pix


class SimpleVBIDataset(BaseVBIDataset):
    """
    A simple VBI dataset with a HPC grid aligned to the pixel axes.
    """

    name = "vbi-simple"

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 2:
            raise ValueError("VBI dataset generator expects two dimensional FITS WCS.")

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for i in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w
