import subprocess
import os


def open_notepad():

    subprocess.Popen("notepad.exe")

    return "Opening Notepad."


def open_calculator():

    subprocess.Popen("calc.exe")

    return "Opening Calculator."


def open_explorer():

    subprocess.Popen("explorer.exe")

    return "Opening File Explorer."


def open_command_prompt():

    subprocess.Popen("cmd.exe")

    return "Opening Command Prompt."


def open_powershell():

    subprocess.Popen("powershell.exe")

    return "Opening PowerShell."


def open_vscode():

    try:
        subprocess.Popen("code")

        return "Opening Visual Studio Code."

    except FileNotFoundError:

        return "Visual Studio Code was not found."

def lock_pc():

    subprocess.run(
        ["rundll32.exe", "user32.dll,LockWorkStation"]
    )

    return "Locking your PC."

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

            subprocess.Popen([path])

            return "Opening Google Chrome."

    return "Google Chrome was not found."


def close_app(app_name):

    process_map = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "calc": "CalculatorApp.exe",
        "vscode": "Code.exe",
        "visual studio code": "Code.exe",
        "powershell": "powershell.exe",
        "cmd": "cmd.exe",
    }

    process_name = process_map.get(
        app_name.lower().strip()
    )

    if not process_name:
        return f"I don't know how to close {app_name}."

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
            return f"Closed {app_name}."

        return f"{app_name} is not running."

    except Exception as e:

        return f"Could not close {app_name}: {e}"

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