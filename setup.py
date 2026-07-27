#!/usr/bin/env python3
"""
Module for setup hostapd shared library
"""

import os
import sys
import shutil
from textwrap import dedent
import tempfile
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools._distutils import sysconfig, ccompiler
from setuptools.errors import CompileError, LinkError

HOSTAPD_DIR = os.path.dirname(os.path.abspath(__file__))
HOSTAPD_SRC = os.path.join(HOSTAPD_DIR, "roguehostapd", "hostapd-2_6", "hostapd", "src")
HOSTAPD_UTILS = os.path.join(HOSTAPD_SRC, "utils")
LIB_NL3_PATH = "/usr/include/libnl3"
LIB_SSL_PATH = "/usr/include/openssl"
SHARED_LIB_PATH = "roguehostapd.hostapd.hostapd"

HOSTAPD_MACROS = [
    ("CONFIG_DRIVER_NL80211", None),
    ("CONFIG_LIBNL32", None),
    ("__linux__", None),
]


def get_all_source_files():
    sources = []
    for root, dirs, files in os.walk(HOSTAPD_SRC):
        for f in files:
            if f.endswith(".c"):
                sources.append(os.path.join(root, f))
    return sources


LIBNL_CODE = dedent("""
#include <netlink/netlink.h>
#include <netlink/genl/genl.h>
int main(int argc, char* argv[])
{
   struct nl_msg *testmsg;
   testmsg = nlmsg_alloc();
   nlmsg_free(testmsg);
   return 0;
}
""")

OPENSSL_CODE = dedent("""
#include <openssl/ssl.h>
#include <openssl/err.h>
int main(int argc, char* argv[])
{
    SSL_load_error_strings();
    return 0;
}
""")


def check_required_library(libname, libraries=None, include_dir=None):
    build_success = True
    tmp_dir = tempfile.mkdtemp(prefix="tmp_" + libname + "_")
    bin_file_name = os.path.join(tmp_dir, "test_" + libname)
    file_name = bin_file_name + ".c"
    code = LIBNL_CODE if libname == "netlink" else OPENSSL_CODE
    with open(file_name, "w") as filep:
        filep.write(code)
    compiler = ccompiler.new_compiler()
    sysconfig.customize_compiler(compiler)
    try:
        compiler.link_executable(
            compiler.compile([file_name], include_dirs=include_dir),
            bin_file_name,
            libraries=libraries,
        )
    except (CompileError, LinkError):
        build_success = False
    finally:
        shutil.rmtree(tmp_dir)
    return build_success


if not check_required_library("netlink", ["nl-3", "nl-genl-3"], [LIB_NL3_PATH]):
    print(
        "[!] The development package for netlink is missing. Please "
        "download it and restart the compilation. "
        "apt-get install libnl-3-dev libnl-genl-3-dev"
    )
    sys.exit(1)

if not check_required_library("openssl", ["ssl"], [LIB_SSL_PATH]):
    print(
        "[!] The development package for openssl is missing. Please "
        "download it and restart the compilation. "
        "apt-get install libssl-dev"
    )
    sys.exit(1)

ext_module = Extension(
    SHARED_LIB_PATH,
    define_macros=HOSTAPD_MACROS,
    libraries=["rt", "ssl", "crypto", "nl-3", "nl-genl-3"],
    sources=get_all_source_files(),
    include_dirs=[HOSTAPD_SRC, HOSTAPD_UTILS, LIB_NL3_PATH],
)

setup(
    ext_modules=[ext_module],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
