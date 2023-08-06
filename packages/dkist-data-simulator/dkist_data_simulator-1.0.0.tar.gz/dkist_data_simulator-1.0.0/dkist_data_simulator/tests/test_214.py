import numpy as np
from astropy.wcs import WCS
import astropy.units as u
import gwcs
import pytest

from dkist_fits_validator import spec214_validator
from dkist_inventory.transforms import TransformBuilder
from dkist_inventory.inventory import sort_headers, extract_inventory

from dkist_data_simulator.spec214 import Spec214Dataset
from dkist_data_simulator.spec214.visp import SimpleVISPDataset
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset
from dkist_data_simulator.spec214.vtf import SimpleVTFDataset
from dkist_data_simulator.spec214.cryo import SimpleCryoDataset
from dkist_data_simulator.spec214.dlnirsp import SimpleDLNIRSPDataset


class DatasetTest214(Spec214Dataset):
    @property
    def fits_wcs(self):
        w = WCS(naxis=2)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = 1, 1
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


@pytest.mark.parametrize("ds", (
    DatasetTest214(dataset_shape=(2, 2, 2, 40, 50),
                   array_shape=(40, 50),
                   time_delta=10
                   ),
    SimpleVISPDataset(n_raster=2,
                      n_scans=3,
                      n_stokes=4,
                      time_delta=10,
                      linewave=500 * u.m
                      ),
    SimpleVISPDataset(n_raster=2,
                      n_scans=3,
                      n_stokes=0,
                      time_delta=10,
                      linewave=500 * u.m
                      ),
    SimpleVBIDataset(n_time=2,
                     time_delta=10,
                     linewave=400 * u.nm
                     ),
    SimpleVTFDataset(n_wave=2,
                     n_repeats=3,
                     n_stokes=4,
                     time_delta=10,
                     linewave=400 * u.nm
                     ),
    SimpleVTFDataset(n_wave=2,
                     n_repeats=3,
                     n_stokes=0,
                     time_delta=10,
                     linewave=400 * u.nm
                     ),
    SimpleCryoDataset(n_raster=2,
                      n_scans=3,
                      n_stokes=4,
                      time_delta=10,
                      linewave=500 * u.m
                      ),
    SimpleCryoDataset(n_raster=2,
                      n_scans=3,
                      n_stokes=0,
                      time_delta=10,
                      linewave=500 * u.m
                      ),
    SimpleDLNIRSPDataset(n_exposures=3,
                         n_stokes=4,
                         time_delta=10,
                         linewave=400 * u.nm
                         ),
    SimpleDLNIRSPDataset(n_exposures=3,
                         n_stokes=0,
                         time_delta=10,
                         linewave=400 * u.nm
                         ),
))
def test_generate_214(ds):
    headers = ds.generate_headers()

    for h in headers:
        spec214_validator.validate(h)

    # Assert that the datasets generated here pass through gwcs generation and inventory creation.
    # This is the most minimal sanity check possible.

    filenames = [f"{i}.fits" for i in range(len(headers))]
    table_headers, _, sorted_headers = sort_headers(headers, filenames)

    wcs = TransformBuilder(sorted_headers).gwcs
    assert isinstance(wcs, gwcs.WCS)

    inv = extract_inventory(table_headers, wcs)
    assert isinstance(inv, dict)
