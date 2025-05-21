import os
import time
import psutil
import subprocess
import platform

from db import get_active_apps_from_db

system = platform.system()

if system == "Windows":
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    REDIRECT_IP = "127.0.0.1"
    paths = {
        "chrome.exe": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "msedge.exe": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "firefox.exe": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "opera.exe": r"%LOCALAPPDATA%\Programs\Opera\launcher.exe",
    }

elif system == "Darwin":
    HOSTS_PATH = "/etc/hosts"
    REDIRECT_IP = "127.0.0.1"
    paths = {
        "Google Chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
        "Safari": "/Applications/Safari.app/Contents/MacOS/Safari",
        "Opera": "/Applications/Opera.app/Contents/MacOS/Opera",
    }

    process_to_app = {
        "chrome.exe": "Google Chrome",
        "firefox.exe": "Firefox",
        "opera.exe": "Opera",
        "safari.exe": "Safari"
    }

else:
    raise RuntimeError(f"Unsupported OS: {system}")

BLOCK_MARKER = "# ANTIPROKRA START"
BLOCK_END = "# ANTIPROKRA END"

browsers = [
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "opera.exe",
]

def filter_items(items, key):
    blocked_items = []
    print(items)

    for item in items:
        print(item)
        if item['is_active'] is True:
            blocked_items.append(item[key])

    return blocked_items

def block_sites(sites):
    with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start = None
    end = None
    for i, line in enumerate(lines):
        if BLOCK_MARKER in line:
            start = i
        if BLOCK_END in line:
            end = i + 1
            break

    if start is not None and end is not None:
        del lines[start:end]

    block_lines = []
    for site in sites:
        block_lines.append(f"{REDIRECT_IP} {site}\n")
        block_lines.append(f"{REDIRECT_IP} www.{site}\n")

    lines.append(f"\n{BLOCK_MARKER}\n")
    lines.extend(block_lines)
    lines.append(f"{BLOCK_END}\n")

    with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Websites blocked via hosts file")

def reset_sites():
    with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start = None
    end = None
    for i, line in enumerate(lines):
        if BLOCK_MARKER in line:
            start = i
        if BLOCK_END in line:
            end = i + 1
            break

    if start is not None and end is not None:
        del lines[start:end]

    with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Websites unblocked (block removed from hosts)")

def get_active_main_browsers():
    found = set()

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in browsers:
                found.add(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return list(found)

def launch_browser(browser_exe):
    if system == "Darwin":
        app_key = process_to_app.get(browser_exe)
        if app_key:
            try:
                subprocess.Popen(["open", "-a", app_key])
            except Exception as e:
                print(f"Failed to launch {app_key}: {e}")
    else:
        path = os.path.expandvars(paths.get(browser_exe, ""))
        if path and os.path.exists(path):
            try:
                subprocess.Popen(path)
            except Exception as e:
                print(f"Failed to launch {browser_exe}: {e}")

def kill_browsers():
    active_browsers = get_active_main_browsers()
    print(active_browsers)

    for browser in active_browsers:
        if system == "Windows":
            os.system(f"taskkill /F /T /IM {browser} >nul 2>&1")
        else:
            browser_name = browser.replace(".exe", "")
            os.system(f"pkill -f {browser_name}")

        time.sleep(0.5)
        launch_browser(browser)

def kill_app_by_name(name):
    name = normalize_exe_name(name)

    for proc in psutil.process_iter(['pid', 'name']):
        proc_name = proc.info['name'].lower()
        if proc_name == name.lower():
            psutil.Process(proc.info['pid']).kill()
            print(f"Killed process: {proc.info['name']} (PID {proc.info['pid']})")

def block_apps(apps):
    while True:
        current_apps = get_active_apps_from_db()
        print(current_apps)
        print(apps)
        if set(current_apps) != set(apps):
            break

        for app in apps:
            kill_app_by_name(app)

        time.sleep(5)

def normalize_exe_name(name):
    if system == "Windows":
        return name if name.lower().endswith(".exe") else name + ".exe"
    return name