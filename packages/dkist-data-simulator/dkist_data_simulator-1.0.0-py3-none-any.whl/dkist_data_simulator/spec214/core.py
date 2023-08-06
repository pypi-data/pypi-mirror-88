import copy
import datetime
from abc import abstractmethod
from typing import Tuple, Literal
from dataclasses import dataclass

import numpy as np  # type: ignore
import astropy.units as u
from dkist_fits_specifications import spec214

from dkist_data_simulator.dataset import Dataset, key_function
from dkist_data_simulator.schemas import Schema, TimeKey
from dkist_data_simulator.spec122 import KNOWN_INSTRUMENT_TABLES

__all__ = ['Spec214Dataset', 'Spec214Schema']


@dataclass(init=False)
class Spec214Schema(Schema):
    """
    A representation of the 214 schema.
    """

    def __init__(self, naxis: int, dnaxis: int, deaxes: int, daaxes: int, instrument=None):
        sections = spec214.load_expanded_spec214(NAXIS=naxis, DNAXIS=dnaxis,
                                                 DEAXES=deaxes, DAAXES=daaxes)
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


class Spec214Dataset(Dataset):
    """
    Generate a collection of FITS files which form a single dataset
    """
    _subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "name") and cls is not Spec214Dataset:
            Spec214Dataset._subclasses[cls.name] = cls

    def __init__(self,
                 dataset_shape: Tuple[int, ...],
                 array_shape: Tuple[int, ...],
                 *,
                 time_delta: float,
                 start_time: datetime.datetime = None,
                 instrument: Literal[tuple(KNOWN_INSTRUMENT_TABLES.keys())] = None):

        self.time_delta = time_delta
        self.start_time = start_time or datetime.datetime.fromisoformat(
            TimeKey("", False, False).generate_value())

        # We have to recalculate a bunch of stuff from the super init here to
        # expand the schema before we call the super constructor.
        data_shape = tuple(d for d in array_shape if d != 1)
        super().__init__(file_schema=Spec214Schema(naxis=len(array_shape),
                                                   dnaxis=len(dataset_shape),
                                                   deaxes=len(array_shape),
                                                   daaxes=len(data_shape),
                                                   instrument=instrument),
                         dataset_shape=dataset_shape,
                         array_shape=array_shape)

        if instrument:
            self.add_constant_key("INSTRUME", KNOWN_INSTRUMENT_TABLES[instrument])
        else:
            self.add_constant_key("INSTRUME")

        self.exposure_time = datetime.timedelta(seconds=1)

        # FITS
        self.add_constant_key("NAXIS", self.array_ndim)
        self.add_constant_key("ORIGIN", "National Solar Observatory")
        self.add_constant_key("TELESCOP", "Daniel K. Inouye Solar Telescope")
        self.add_constant_key("OBSRVTRY", "Haleakala High Altitude Observatory Site")

        # WCS
        self.add_constant_key("CRDATEn")

        # Datacenter
        self.add_constant_key("DSETID")
        self.add_constant_key("RRUNID")
        self.add_constant_key("RECIPEID")
        self.add_constant_key("RINSTID")
        self.add_constant_key("PROP_ID")
        self.add_constant_key("EXPER_ID")

        # Dataset
        self.add_constant_key("DNAXIS", self.dataset_ndim)
        self.add_constant_key("DAAXES", self.data_ndim)
        self.add_constant_key("DEAXES", self.dataset_ndim - self.data_ndim)
        self.add_constant_key("LEVEL", 1)

        # k index keys, which is a subset of d
        for k in range(self.data_ndim + 1, self.dataset_ndim + 1):
            self.add_generator_function(f"DINDEX{k}", type(self).dindex)

        # dtypes need to be generated as a coherent set, so it needs state
        self._dtypes = None

        # d index keys
        for d in range(1, self.dataset_ndim + 1):
            self.add_generator_function(f"DNAXIS{d}", type(self).dnaxis)
            self.add_generator_function(f"DTYPE{d}", type(self).dtype)
            self.add_generator_function(f"DUNIT{d}", type(self).dunit)
            self.add_constant_key(f"DWNAME{d}")
            self.add_constant_key(f"DPNAME{d}")

    @property
    def data(self):
        return np.empty(self.array_shape)

    ###########################################################################
    # FITS
    ###########################################################################
    @key_function("DATE")
    def date(self, key: str):
        return datetime.datetime.now().isoformat('T')

    @key_function(
        "DATE-BEG",
        "DATE-AVG",
        "DATE-END",
    )
    def date_obs(self, key: str):
        delta = datetime.timedelta(seconds=self.index * self.time_delta)
        frame_start = self.start_time + delta
        frame_end = frame_start + self.exposure_time

        if key == "DATE-BEG":
            ret = frame_start

        if key == "DATE-AVG":
            ret = frame_start + ((frame_end - frame_start) / 2)

        if key == "DATE-END":
            ret = frame_end

        return ret.isoformat('T')

    @key_function("NAXISn")
    def naxis(self, key: str):
        fits_ind = int(key[-1])
        ind = self.array_ndim - fits_ind
        return self.array_shape[ind]

    ###########################################################################
    # WCS
    ###########################################################################
    @property
    @abstractmethod
    def fits_wcs(self):
        """
        A FITS WCS object for the current frame.
        """

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

    ###########################################################################
    # Dataset
    ###########################################################################
    def dnaxis(self, key: str):
        fits_ind = int(key[-1])
        ind = self.dataset_ndim - fits_ind
        return int(self.dataset_shape[ind])

    def dindex(self, key: str):
        fits_ind = int(key[-1])
        # While not all indices are generated, they count with the d index.
        ind = self.dataset_ndim - fits_ind
        return int(self.file_index[ind])

    def _not_spatial_dtype(self):
        """Generate a random dtype which isn't spatial."""
        dtype = self.file_schema["DTYPE1"].generate_value()
        if dtype == "SPATIAL":
            return self._not_spatial_dtype()
        return dtype

    def dtype(self, key: str):
        """
        Generate a random set of types and then sanitise the number and
        position of any spatial axes.
        """
        wapt_translation = {
            "pos": "SPATIAL",
            "em": "SPECTRAL",
            "time": "TEMPORAL"
        }

        if self._dtypes is None:
            self._dtypes = []
            for wapt in self.fits_wcs.world_axis_physical_types:
                atype = tuple(filter(lambda x: x[0] in wapt, wapt_translation.items()))[0]
                self._dtypes.append(atype[1])

            if not self._dtypes.count("SPATIAL") == 2:
                raise ValueError("It is expected the FITS WCS describe both spatial dimensions")

            for _ in range(len(self._dtypes), self.dataset_ndim):
                self._dtypes.append(self._not_spatial_dtype())

            if "TEMPORAL" not in self._dtypes and "SPECTRAL" in self._dtypes:
                self._dtypes[self._dtypes.index("SPECTRAL")] = "TEMPORAL"

            if "TEMPORAL" not in self._dtypes:
                self._dtypes[self._dtypes.index("STOKES")] = "TEMPORAL"


        return self._dtypes[int(key[-1]) - 1]

    def dunit(self, key: str):
        d = int(key[-1])
        type_unit_map = {
            "SPATIAL": u.arcsec,
            "SPECTRAL": u.nm,
            "TEMPORAL": u.s,
            "STOKES": u.one
        }
        dtype = self.dtype(f"DTYPE{d}")
        return type_unit_map[dtype].to_string(format='fits')
