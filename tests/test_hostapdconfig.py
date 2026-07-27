import unittest


class TestHostapdConfig(unittest.TestCase):
    """Smoke tests for HostapdConfig"""

    def test_imports(self):
        from roguehostapd.config.hostapdconfig import HostapdConfig

        config = HostapdConfig()
        config.init_config()
        self.assertIn("ssid", config.configuration_dict)

    def test_default_settings(self):
        from roguehostapd.config.hostapdconfig import HOSTAPD_DIR

        self.assertTrue(HOSTAPD_DIR.endswith("hostapd-2_6"))
