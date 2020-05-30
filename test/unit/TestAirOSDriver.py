import unittest

from napalm_airos import airos
from napalm.base.test.base import TestConfigNetworkDriver, TestGettersNetworkDriver # noqa


class TestConfigAirOSDriver(unittest.TestCase, TestConfigNetworkDriver):

    @classmethod
    def setUpClass(cls):
        """Executed when the class is instantiated."""
        cls.vendor = 'airos'
        cls.device = airos.AirOSDriver(
            '127.0.0.1',
            'vagrant',
            'vagrant',
            timeout=60,
            optional_args={
                'port': 22,
            },
        )
        cls.device.open()
