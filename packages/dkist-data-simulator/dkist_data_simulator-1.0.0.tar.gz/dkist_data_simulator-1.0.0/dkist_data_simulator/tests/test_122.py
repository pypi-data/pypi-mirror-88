from dkist_fits_validator import spec122_validator

from dkist_data_simulator.spec122 import Spec122Dataset


def test_generate_122():
    ds = Spec122Dataset(time_delta=10,
                        dataset_shape=[16, 2048, 4096],
                        array_shape=[1, 2048, 4096],
                        instrument='vbi')
    headers = ds.generate_headers(required_only=True)
    for h in headers:
        spec122_validator.validate(h)
        assert h['NAXIS'] == 3
        assert h['NAXIS1'] == 4096
        assert h['NAXIS2'] == 2048
        assert h['NAXIS3'] == 1
        assert h['INSTRUME'] == 'VBI'
