import subprocess
import os
import shutil


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

    # Try PATH
    chrome_command = shutil.which("chrome")

    if chrome_command:

        try:
            subprocess.Popen([chrome_command])
            return "Opening Google Chrome."
        except Exception:
            pass

    return "Google Chrome was not found."


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