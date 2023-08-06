import astropy.units as u

from dkist_inventory.transforms import TransformBuilder
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset

ds = SimpleVBIDataset([10, 4096, 4096], [4096, 4096], 1, linewave=456*u.nm)
headers = ds.generate_headers()

tf = TransformBuilder(headers)
print(repr(tf.gwcs))
