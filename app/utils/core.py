import re
import uuid
import platform
import psutil as ps
import pywinctl as pwc
import pythoncom
from functools import wraps
import subprocess
import time
from typing import Any
from datetime import datetime
import threading
from typing import Callable


def run_in_com(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        pythoncom.CoInitialize()
        try:
            return func(*args, **kwargs)
        finally:
            pythoncom.CoUninitialize()

    return wrapper


def track_apps_usage(stop_event: threading.Event, usage_data: dict[str, Any]):
    while not stop_event.is_set():
        current_apps = get_running_applications()
        now = datetime.now()

        new_apps = {k: v for k, v in current_apps.items() if k not in usage_data}
        apps_to_continue = {k: v for k, v in usage_data.items() if k in current_apps}
        apps_to_end = {k: v for k, v in usage_data.items() if k not in current_apps}

        for app_key, app_data in new_apps.items():
            app_data["tracking"].append({"start": now})
            usage_data[app_key] = app_data

        for app_key, app_data in apps_to_continue.items():
            if len(app_data["tracking"]) == 0 or (
                "end" in app_data["tracking"][-1].keys()
            ):
                app_data["tracking"].append({"start": now})

        for app_key, app_data in apps_to_end.items():
            if len(app_data["tracking"]) != 0:
                app_data["tracking"][-1].update({"end": now})

        time.sleep(2)


def end_apps_usage(usage_data: dict[str, Any]) -> dict[str, Any]:
    for _, app_data in usage_data.items():
        now = datetime.now()
        for track in app_data["tracking"]:
            if "end" not in track.keys():
                track["end"] = now

    return usage_data


def get_mac_address() -> str:
    return ":".join(re.findall("..", "%012x" % uuid.getnode()))


def get_device_data() -> dict[str, Any]:
    device_info = dict()
    device_info["mac-address"] = get_mac_address()
    device_info["os_name"] = platform.system()
    device_info["os_release"] = platform.release()
    device_info["os_release_ver"] = platform.version()
    device_info["architecture"] = platform.machine()
    return device_info


@run_in_com
def get_running_applications() -> dict[str, Any]:
    apps_data_dict = dict()

    for window in pwc.getAllWindows():
        try:
            pid = window.getPID()
            proc = ps.Process(pid)
            exe_path = proc.exe()

            key = f"{exe_path}_{pid}"

            if key not in apps_data_dict:
                apps_data_dict[key] = {
                    "exe": exe_path,
                    "name": proc.name(),
                    "cmdline": " ".join(proc.cmdline()),
                    "windows": [],
                }

            if (
                window.isAlive
                and (window.isActive or window.isVisible)
                and (window.isMinimized or window.isMaximized)
                and window.title
            ):
                apps_data_dict[key]["windows"].append(window)

        except (ps.NoSuchProcess, ps.AccessDenied, ValueError):
            continue

    apps_data_dict = {
        key.split("_")[0]: {
            "exe": app["exe"],
            "name": app["name"],
            "cmdline": app["cmdline"],
            "tracking": [],
        }
        for key, app in apps_data_dict.items()
        if len(app["windows"]) != 0
    }

    return apps_data_dict


def run_applications(apps: list[dict[str, Any]]):
    current_apps = get_running_applications()

    for app in apps:
        if app["exe"] in [a["exe"] for a in current_apps.values()]:
            continue
        subprocess.call(app["cmdline"].split())
