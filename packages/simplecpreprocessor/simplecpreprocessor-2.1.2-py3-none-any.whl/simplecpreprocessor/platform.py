from __future__ import absolute_import
import platform
from simplecpreprocessor.exceptions import UnsupportedPlatform


def extract_platform_spec():
    system = platform.system()
    bitness, _ = platform.architecture()
    return system, bitness


def calculate_windows_constants(bitness):
    constants = {}
    if bitness == "32bit":
        constants.update({
            "_WIN32": "1",
        })
    elif bitness == "64bit":
        constants.update({
            "_WIN64": "1",
        })
    else:
        raise UnsupportedPlatform("Unsupported bitness %s" % str(bitness))
    return constants


def calculate_linux_constants(bitness):
    constants = {
        "__linux__": "__linux__"
    }
    if bitness == "32bit":
        constants.update({
            "__i386__": "1",
            "__i386": "1",
            "i386": "1",
        })
    elif bitness == "64bit":
        constants.update({
            "__x86_64__": "1",
            "__x86_64": "1",
            "__amd64__": "1",
            "__amd64": "1",
        })
    else:
        raise UnsupportedPlatform("Unsupported bitness %s" % str(bitness))
    return constants


def calculate_platform_constants():
    system, bitness = extract_platform_spec()
    if system == "Windows":
        constants = calculate_windows_constants(bitness)
    elif system == "Linux":
        constants = calculate_linux_constants(bitness)
    else:
        raise UnsupportedPlatform("Unsupported platform %s" % system)
    constants["__SIZE_TYPE__"] = "size_t"
    return constants


PLATFORM_CONSTANTS = calculate_platform_constants()
