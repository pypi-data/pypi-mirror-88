import copy
import datetime
from typing import Tuple, Literal
from dataclasses import dataclass

import numpy as np  # type: ignore
from astropy.wcs import WCS  # type: ignore
from dkist_fits_specifications import spec122

from dkist_data_simulator.dataset import Dataset, key_function
from dkist_data_simulator.schemas import Schema, TimeKey

__all__ = ['Spec122Dataset', 'Spec122Schema']


KNOWN_INSTRUMENT_TABLES = {
    'vbi': 'VBI',
    'visp': 'VISP',
    'dlnirsp': 'DL-NIRSP',
    'cryonirsp': 'CRYO-NIRSP',
    'vtf': 'VTF',
}


@dataclass(init=False)
class Spec122Schema(Schema):
    """
    A representation of the 122 schema.
    """

    def __init__(self, instrument=None):
        sections = spec122.load_spec122()
        if instrument:
            if instrument not in KNOWN_INSTRUMENT_TABLES.keys():
                raise ValueError(
                    f"{instrument} does not match one of the known "
                    "instrument table names: {tuple(KNOWN_INSTRUMENT_TABLES.keys())}"
                )
            for table in KNOWN_INSTRUMENT_TABLES.keys():
                if table == instrument:
                    continue
                sections.pop(table)

        super().__init__(self.sections_from_dicts(sections.values()))


class Spec122Dataset(Dataset):
    """
    Generate a collection of FITS files which form a single "dataset" or
    instrument program.

    Parameters
    ----------
    dataset_shape
        The full shape of the dataset, including all dimensions, i.e. the size
        of the reconstructed array when all files are combined. For 122 files
        is normally ``(N, yshape, xshape)``, where ``N`` is the number of files
        to be generated and the last two dimensions are the data size, minus
        any dummy dimensions.
    array_shape
        The shape of the array in the files.
    time_delta
        The time in s between each frame
    start_time
        The timestamp of the first frame
    instrument
        The name of the instrument, must match one of the instrument tables. If
        `None` all instrument tables will be used.

    """

    def __init__(self,
                 dataset_shape: Tuple[int, ...],
                 array_shape: Tuple[int, ...],
                 time_delta: float,
                 start_time: datetime.datetime = None,
                 instrument: Literal[tuple(KNOWN_INSTRUMENT_TABLES.keys())] = None):

        self.time_delta = time_delta
        self.start_time = start_time or datetime.datetime.fromisoformat(
            TimeKey("", False, False).generate_value())

        super().__init__(file_schema=Spec122Schema(instrument),
                         dataset_shape=dataset_shape,
                         array_shape=array_shape)

        end_time = self.start_time + datetime.timedelta(seconds=self.n_files * self.time_delta)

        # FITS
        self.add_constant_key("NAXIS", self.array_ndim)
        self.add_constant_key("NAXIS1", self.array_shape[2])
        self.add_constant_key("NAXIS2", self.array_shape[1])
        self.add_constant_key("NAXIS3", self.array_shape[0])
        self.add_constant_key("DATE-BGN", self.start_time.isoformat('T'))
        self.add_constant_key("DATE-END", end_time.isoformat('T'))
        self.add_constant_key("ORIGIN", "National Solar Observatory")
        self.add_constant_key("TELESCOP", "Daniel K. Inouye Solar Telescope")
        self.add_constant_key("OBSERVAT", "Haleakala High Altitude Observatory Site")
        if instrument:
            self.add_constant_key("INSTRUME", KNOWN_INSTRUMENT_TABLES[instrument])

        # WCS
        self.add_constant_key("CRDATEn")

    @property
    def data(self):
        return np.empty(self.array_shape)

    ###########################################################################
    # FITS
    ###########################################################################
    @key_function("DATE")
    def date(self, key: str):
        return datetime.datetime.now().isoformat('T')

    @key_function("DATE-OBS")
    def date_obs(self, key: str):
        return (self.start_time + datetime.timedelta(seconds=self.index * self.time_delta)).isoformat('T')

    ###########################################################################
    # WCS
    ###########################################################################
    @property
    def fits_wcs(self):
        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[2] / 2, self.array_shape[1] / 2, 1
        w.wcs.crval = 0, 0, 0
        w.wcs.cdelt = 1, 1, 1
        w.wcs.cunit = "arcsec", "arcsec", "m"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN", "None"
        w.wcs.pc = np.identity(self.array_ndim)
        return w

    @key_function(
        "WCSAXES",
        "CRPIXn",
        "CRVALn",
        "CDELTn",
        "CUNITn",
        "CTYPEn",
    )
    def wcs_keys(self, key: str):
        return self.fits_wcs.to_header()[key]

    @key_function(
        "LONPOLE",
    )
    def wcs_set_keys(self, key: str):
        wcs = copy.deepcopy(self.fits_wcs)
        wcs.wcs.set()
        return wcs.to_header()[key]

    @key_function("PCi_j")
    def pc_keys(self, key: str):
        i = self.array_ndim - int(key[2])
        j = self.array_ndim - int(key[-1])
        default = self.fits_wcs.wcs.pc[j, i]
        return self.fits_wcs.to_header().get(key, default)
