import os
import time
import psutil
import subprocess

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

REDIRECT_IP = "127.0.0.1"  
BLOCK_MARKER = "# ANTIPROKRA START"
BLOCK_END = "# ANTIPROKRA END"

browsers = [
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "opera.exe",
    "yandex.exe"  
]

paths = {
    "chrome.exe": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge.exe": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "firefox.exe": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "opera.exe": r"%LOCALAPPDATA%\Programs\Opera\launcher.exe",
    "yandex.exe": r"%LOCALAPPDATA%\Yandex\YandexBrowser\Application\browser.exe"
}

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

    print("Сайты заблокированы через hosts")

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
    path = os.path.expandvars(paths.get(browser_exe, ""))
    if path and os.path.exists(path):
        try:
            subprocess.Popen(path)
        except Exception as e:
            print(f"Ошибка запуска {browser_exe}: {e}")

def killBrowsers():
    active_browsers = get_active_main_browsers()
    print(active_browsers)

    for i in range(len(active_browsers)):
        os.system(f"taskkill /F /T /IM {active_browsers[i]} >nul 2>&1")
        time.sleep(0.5)
        launch_browser(active_browsers[i])