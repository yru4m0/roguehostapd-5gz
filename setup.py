"""
Module for setup hostapd shared library
"""

import shutil

from setuptools import setup
from distutils.command.build_ext import build_ext
import roguehostapd.buildutil.buildcommon as buildcommon
import roguehostapd.buildutil.buildexception as buildexception
from roguehostapd.config.hostapdconfig import WHITE, RED

# define project information
NAME = "roguehostapd"
PACKAGES = ["roguehostapd", "examples", "roguehostapd.config", "roguehostapd.buildutil"]
PACKAGE_DIR = {"roguehostapd": "roguehostapd"}
PACKAGE_DATA = {"roguehostapd": ["config/hostapd.conf", "config/config.ini"]}
VERSION = "1.1.2"
DESCRIPTION = "Hostapd wrapper for hostapd"
URL = "https://github.com/wifiphisher/roguehostapd"
AUTHOR = "Anakin"

try:
    EXT_MODULE = buildcommon.get_extension_module()
    setup(
        name=NAME,
        packages=PACKAGES,
        package_dir=PACKAGE_DIR,
        package_data=PACKAGE_DATA,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        install_requires=[],
        zip_safe=False,
        cmdclass={"build_ext": build_ext},
        ext_modules=EXT_MODULE,
    )
except buildexception.SharedLibMissError as exobj:
    RED = "\033[31m"
    WHITE = "\033[0m"
