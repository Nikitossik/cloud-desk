import re
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
import shlex
import platform
import uuid

EXE_BLACKLIST = {
    "applicationframehost.exe",
    "RuntimeBroker.exe",
    "ShellExperienceHost.exe",
    "StartMenuExperienceHost.exe",
    "SearchHost.exe",
}

def get_mac_address() -> str:
    return ":".join(re.findall("..", "%012x" % uuid.getnode()))

def get_device_data() -> dict[str, Any]:
    device_info = dict()
    device_info["mac_address"] = get_mac_address() 
    # device_info["os_name"] = "Darwin" # test macOs
    device_info["os_name"] = platform.system()
    device_info["os_release"] = platform.release()
    device_info["os_release_ver"] = platform.version()
    device_info["architecture"] = platform.machine()
    return device_info

def run_in_com(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        pythoncom.CoInitialize()
        try:
            return func(*args, **kwargs)
        finally:
            pythoncom.CoUninitialize()

    return wrapper

@run_in_com
def get_running_applications() -> dict[str, Any]:
    apps_data_dict = dict()

    for window in pwc.getAllWindows():
        try:
            pid = window.getPID()
            proc = ps.Process(pid)
            proc_name = (proc.name() or "").lower()

            if proc_name in EXE_BLACKLIST:
                continue

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

def run_applications(apps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    current_apps = get_running_applications()
    current_exes = {a["exe"] for a in current_apps.values()}

    results = []

    for app in apps:
        app_id = app.get("app_id")
        state_id = app.get("state_id")
        exe = app.get("exe")
        cmdline = app.get("cmdline") or ""
        name = app.get("name") or exe
        is_active = bool(app.get("is_active"))
        display_name = app.get("display_name")

        base_result = {
            "app_id": app_id,
            "state_id": state_id,
            "exe": exe,
            "name": name,
            "is_active": is_active,
            "display_name": display_name,
        }

        def append_result(status: str, reason: str | None = None):
            results.append({
                **base_result,
                "status": status,
                "reason": reason,
            })

        if exe in current_exes:
            append_result("already_running")
            continue

        try:
            args = shlex.split(cmdline, posix=False) if cmdline else [exe]
            if not args:
                args = [exe]

            subprocess.Popen(args)
            append_result("started")

        except PermissionError as e:
            append_result("failed_access_denied", str(e))
        except FileNotFoundError as e:
            append_result("failed_not_found", str(e))
        except Exception as e:
            append_result("failed_exception", str(e))

    return results