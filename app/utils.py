import re
import uuid
import platform
import psutil
import pywinctl as pwc
import pythoncom
from functools import wraps


def run_in_com(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pythoncom.CoInitialize()
        try:
            return func(*args, **kwargs)
        finally:
            pythoncom.CoUninitialize()

    return wrapper


def get_mac_address():
    return ":".join(re.findall("..", "%012x" % uuid.getnode()))


def get_device_info():
    device_info = dict()
    device_info["mac-address"] = get_mac_address()
    device_info["os_name"] = platform.system()
    device_info["os_release"] = platform.release()
    device_info["os_release_ver"] = platform.version()
    device_info["architecture"] = platform.machine()
    return device_info


@run_in_com
def get_running_applications():
    apps_data = pwc.getAllWindowsDict(tryToFilter=True)
    applications = []

    for _, app_info in apps_data.items():
        if not psutil.pid_exists(app_info["pìd"]):
            continue

        app_proc = psutil.Process(app_info["pìd"])
        applications.append(
            {
                "exe": app_proc.exe(),
                "cmdline": " ".join(app_proc.cmdline()),
                "name": app_proc.name(),
                # "username": app_proc.username(), don't need it for now
                # "windows": app_info["windows"], # for later
            }
        )

    return applications
