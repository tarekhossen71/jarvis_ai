import subprocess
import os
import shutil
import pygetwindow as gw
import pyautogui

# =========================================================
# BASIC APPLICATIONS
# =========================================================

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."
    except Exception as e:
        return f"Could not open Notepad: {e}"


def open_calculator():
    try:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."
    except Exception as e:
        return f"Could not open Calculator: {e}"


def open_explorer():
    try:
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer."
    except Exception as e:
        return f"Could not open File Explorer: {e}"


def open_command_prompt():
    try:
        subprocess.Popen(["cmd.exe"])
        return "Opening Command Prompt."
    except Exception as e:
        return f"Could not open Command Prompt: {e}"


def open_powershell():
    try:
        subprocess.Popen(["powershell.exe"])
        return "Opening PowerShell."
    except Exception as e:
        return f"Could not open PowerShell: {e}"


# =========================================================
# VS CODE
# =========================================================

def open_vscode():
    # 1. Try PATH
    code_command = shutil.which("code")

    if code_command:
        try:
            subprocess.Popen([code_command])
            return "Opening Visual Studio Code."
        except Exception:
            pass

    # 2. Common installation locations
    possible_paths = [
        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles%\Microsoft VS Code\Code.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles(x86)%\Microsoft VS Code\Code.exe"
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                subprocess.Popen([path])
                return "Opening Visual Studio Code."
            except Exception:
                continue

    return "Visual Studio Code was not found."


# =========================================================
# CHROME
# =========================================================

def open_chrome():

    import psutil

    # =========================================
    # Check if Chrome is already running
    # =========================================

    for process in psutil.process_iter(["name"]):

        try:
            process_name = process.info["name"]

            if process_name and process_name.lower() == "chrome.exe":
                return "Google Chrome is already open."

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # =========================================
    # Chrome paths
    # =========================================

    chrome_paths = [
        os.path.expandvars(
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    for path in chrome_paths:

        if os.path.exists(path):

            try:
                subprocess.Popen([path])
                return "Opening Google Chrome."

            except Exception:
                continue

    # =========================================
    # Try PATH
    # =========================================

    chrome_command = shutil.which("chrome")

    if chrome_command:

        try:
            subprocess.Popen([chrome_command])
            return "Opening Google Chrome."

        except Exception:
            pass

    return "Google Chrome was not found."


def open_firefox():

    import psutil

    # =========================================
    # Check if Firefox is already running
    # =========================================

    for process in psutil.process_iter(["name"]):

        try:
            process_name = process.info["name"]

            if process_name and process_name.lower() == "firefox.exe":
                return "Firefox is already open."

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # =========================================
    # Firefox paths
    # =========================================

    firefox_paths = [
        os.path.expandvars(
            r"%ProgramFiles%\Mozilla Firefox\firefox.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe"
        ),
    ]

    for path in firefox_paths:

        if os.path.exists(path):

            try:
                subprocess.Popen([path])
                return "Opening Firefox."

            except Exception:
                continue

    # =========================================
    # Try PATH
    # =========================================

    firefox_command = shutil.which("firefox")

    if firefox_command:

        try:
            subprocess.Popen([firefox_command])
            return "Opening Firefox."

        except Exception:
            pass

    return "Firefox was not found."
# =========================================================
# DYNAMIC APPLICATION OPENER
# =========================================================

def open_application(app_name):

    app_name = app_name.strip()

    if not app_name:
        return "Please provide an application name."

    normalized = app_name.lower()

    # Common aliases
    aliases = {
        "vscode": "Visual Studio Code",
        "vs code": "Visual Studio Code",
        "visual studio code": "Visual Studio Code",

        "chrome": "Google Chrome",
        "google chrome": "Google Chrome",

        "firefox": "Firefox",
        "mozilla firefox": "Firefox",

        "notepad": "Notepad",

        "calculator": "Calculator",
        "calc": "Calculator",

        "explorer": "File Explorer",
        "file explorer": "File Explorer",

        "cmd": "Command Prompt",
        "command prompt": "Command Prompt",

        "powershell": "PowerShell",
    }

    display_name = aliases.get(normalized, app_name)

    # -----------------------------------------------------
    # Known applications
    # -----------------------------------------------------

    if normalized in [
        "vscode",
        "vs code",
        "visual studio code"
    ]:
        return open_vscode()

    if normalized in [
        "chrome",
        "google chrome"
    ]:
        return open_chrome()

    if normalized in [
        "firefox",
        "mozilla firefox"
    ]:
        return open_firefox()

    if normalized == "notepad":
        return open_notepad()

    if normalized in [
        "calculator",
        "calc"
    ]:
        return open_calculator()

    if normalized in [
        "explorer",
        "file explorer"
    ]:
        return open_explorer()

    if normalized in [
        "cmd",
        "command prompt"
    ]:
        return open_command_prompt()

    if normalized == "powershell":
        return open_powershell()

    # -----------------------------------------------------
    # Try Windows PATH
    # -----------------------------------------------------

    command = shutil.which(app_name)

    if command:

        try:
            subprocess.Popen([command])
            return f"Opening {display_name}."
        except Exception:
            pass

    # -----------------------------------------------------
    # Try Windows Start Menu / App Paths
    # -----------------------------------------------------

    start_menu_paths = [
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),
        os.path.expandvars(
            r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"
        ),
    ]

    app_lower = normalized.replace(" ", "")

    for start_menu in start_menu_paths:

        if not os.path.exists(start_menu):
            continue

        for root, dirs, files in os.walk(start_menu):

            for file in files:

                if not file.lower().endswith((
                    ".lnk",
                    ".exe",
                    ".appref-ms"
                )):
                    continue

                filename = os.path.splitext(file)[0]
                filename_normalized = filename.lower().replace(
                    " ",
                    ""
                )

                if (
                    app_lower in filename_normalized
                    or filename_normalized in app_lower
                ):

                    path = os.path.join(root, file)

                    try:

                        os.startfile(path)

                        return f"Opening {display_name}."

                    except Exception:
                        continue

    return (
        f"I couldn't find {display_name}. "
        f"Please make sure the application is installed."
    )


# =========================================================
# CLOSE APPLICATION
# =========================================================

def close_app(app_name):

    app_name = app_name.lower().strip()

    process_map = {

        "chrome": ["chrome.exe"],
        "google chrome": ["chrome.exe"],

        "notepad": ["notepad.exe"],

        "calculator": ["CalculatorApp.exe"],
        "calc": ["CalculatorApp.exe"],

        "vscode": ["Code.exe"],
        "vs code": ["Code.exe"],
        "visual studio code": ["Code.exe"],

        "powershell": ["powershell.exe"],

        "cmd": ["cmd.exe"],
        
        "laragon": [
            "laragon.exe",
            "laragon.exe",
            "nginx.exe",
            "httpd.exe",
            "mysqld.exe"
        ],

        "xampp": [
            "xampp-control.exe",
            "httpd.exe",
            "mysqld.exe"
        ],

        "telegram": [
            "Telegram.exe"
        ],

        "postman": [
            "Postman.exe"
        ],

        "spotify": [
            "Spotify.exe"
        ],
    }

    processes = process_map.get(app_name)

    if not processes:

        # Try direct process name
        possible_process = app_name.replace(" ", "") + ".exe"

        try:

            result = subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    possible_process,
                    "/F"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return f"Closed {app_name}."

        except Exception:
            pass

        return f"I don't know how to close {app_name}."

    closed = False

    for process_name in processes:

        try:

            result = subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    process_name,
                    "/F"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                closed = True

        except Exception:
            continue

    if closed:
        return f"Closed {app_name}."

    return f"{app_name} is not running."


# =========================================================
# SYSTEM
# =========================================================

def lock_pc():

    try:

        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll,LockWorkStation"
            ]
        )

        return "Locking your PC."

    except Exception as e:

        return f"Could not lock PC: {e}"


def minimize_all_windows():

    try:

        subprocess.run(
            [
                "powershell",
                "-Command",
                "(New-Object -ComObject Shell.Application).MinimizeAll()"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        return "Minimizing all windows."

    except Exception as e:

        return f"Could not minimize windows: {e}"


def show_desktop():

    try:

        subprocess.run(
            [
                "powershell",
                "-Command",
                "(New-Object -ComObject Shell.Application).ToggleDesktop()"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        return "Showing desktop."

    except Exception as e:

        return f"Could not show desktop: {e}"



def minimize_application(app_name):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:

        title = window.title.lower()

        if app_name in title:

            if window.isMinimized:
                return f"{app_name} is already minimized."

            window.minimize()

            return f"Minimized {app_name}."

    return f"I could not find {app_name}."


def maximize_application(app_name):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:

        title = window.title.lower()

        if app_name in title:

            window.restore()
            window.maximize()

            return f"Maximized {app_name}."

    return f"I could not find {app_name}."


def switch_to_application(app_name):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:

        title = window.title.lower()

        if app_name in title:

            try:
                if window.isMinimized:
                    window.restore()

                window.activate()

                return f"Switched to {app_name}."

            except Exception as e:
                return f"I found {app_name}, but could not switch to it."

    return f"I could not find {app_name}."

def get_active_window():
    try:
        window = gw.getActiveWindow()

        if window is None:
            return "I could not detect the active window."

        title = window.title.strip()

        if not title:
            return "The active window has no title."

        return f"The active window is {title}."

    except Exception as e:
        return "I could not detect the active window."


def switch_to_next_window():
    try:
        import pyautogui

        pyautogui.hotkey("alt", "tab")

        return "Switched to the next window."

    except Exception as e:
        return "I could not switch to the next window."


def switch_to_previous_window():
    try:
        import pyautogui

        # Windows-এর Shift + Alt + Tab
        pyautogui.keyDown("shift")
        pyautogui.hotkey("alt", "tab")
        pyautogui.keyUp("shift")

        return "Switched to the previous window."

    except Exception as e:
        return "I could not switch to the previous window."

def get_open_windows():
    try:
        windows = gw.getAllWindows()

        titles = []

        for window in windows:
            title = window.title.strip()

            if title and title not in titles:
                titles.append(title)

        if not titles:
            return "I could not find any open windows."

        result = "Open windows are:\n"

        for index, title in enumerate(titles, start=1):
            result += f"{index}. {title}\n"

        return result.strip()

    except Exception:
        return "I could not get the list of open windows."

def restore_all_windows():
    try:
        windows = gw.getAllWindows()

        restored = 0

        for window in windows:
            try:
                if window.isMinimized:
                    window.restore()
                    restored += 1
            except Exception:
                continue

        if restored == 0:
            return "There are no minimized windows to restore."

        return f"Restored {restored} window(s)."

    except Exception:
        return "I could not restore the windows."

def move_application(app_name, x, y):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:
        title = window.title.lower()

        if app_name in title:
            try:
                window.moveTo(x, y)
                return f"Moved {app_name} to position {x}, {y}."
            except Exception:
                return f"I found {app_name}, but could not move it."

    return f"I could not find {app_name}."