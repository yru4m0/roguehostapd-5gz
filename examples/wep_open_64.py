"""
Example for lunching the WEP-OPEN-64 Access Point
"""

from roguehostapd.apctrl import Hostapd

if __name__ == "__main__":
    HOSTAPD_CONFIG = {
        "ssid": "test",
        "interface": "wlan12",
        "wep_default_key": "0",
        "wep_key0": '"abcde"',
    }
    HOSTAPD_OBJ = Hostapd()
    HOSTAPD_OBJ.start(HOSTAPD_CONFIG, {})
