from ctypes import POINTER, cast
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, CoCreateInstance
from datetime import datetime
import subprocess
import psutil
import shutil
import pyautogui
import os
import pyperclip
import speedtest


def get_time():

    return datetime.now().strftime("%I:%M %p")


def get_date():

    return datetime.now().strftime("%d %B %Y")


def lock_pc():

    subprocess.run(
        ["rundll32.exe", "user32.dll,LockWorkStation"]
    )

    return "Locking your PC."

def shutdown_pc():

    subprocess.run(
        ["shutdown", "/s", "/t", "0"]
    )

    return "Shutting down your PC."


def restart_pc():

    subprocess.run(
        ["shutdown", "/r", "/t", "0"]
    )

    return "Restarting your PC."

def get_battery_status():

    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is not available."

    percentage = battery.percent

    if battery.power_plugged:
        status = "charging"
    else:
        status = "not charging"

    return f"Your battery is {percentage}% and it is {status}."


def get_cpu_usage():

    usage = psutil.cpu_percent(interval=1)

    return f"CPU usage is {usage}%."


def get_ram_usage():

    memory = psutil.virtual_memory()

    used_gb = memory.used / (1024 ** 3)
    total_gb = memory.total / (1024 ** 3)
    percentage = memory.percent

    return (
        f"RAM usage is {percentage}%. "
        f"You are using {used_gb:.2f} GB "
        f"out of {total_gb:.2f} GB."
    )


def get_disk_space():

    disk = shutil.disk_usage("C:\\")

    free_gb = disk.free / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)

    return (
        f"Your C drive has {free_gb:.2f} GB free "
        f"out of {total_gb:.2f} GB."
    )


def get_internet_status():

    try:

        import socket

        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        return "Your internet connection is working."

    except OSError:

        return "Your internet connection is not available."


from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()

    interface = devices._dev.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    return cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )


def get_volume():
    volume = get_volume_interface()

    current_volume = volume.GetMasterVolumeLevelScalar()

    percentage = round(current_volume * 100)

    return f"Current volume is {percentage} percent."


def set_volume(level):
    try:
        level = int(level)
        level = max(0, min(level, 100))

        volume = get_volume_interface()

        volume.SetMasterVolumeLevelScalar(
            level / 100,
            None
        )

        return f"Volume set to {level} percent."

    except ValueError:
        return "Please provide a valid volume percentage."


def increase_volume():
    volume = get_volume_interface()

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.10, 1.0)

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    return f"Volume increased to {round(new_volume * 100)} percent."


def decrease_volume():
    volume = get_volume_interface()

    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.10, 0.0)

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    return f"Volume decreased to {round(new_volume * 100)} percent."


def mute_volume():
    volume = get_volume_interface()
    volume.SetMute(1, None)

    return "Volume muted."


def unmute_volume():
    volume = get_volume_interface()
    volume.SetMute(0, None)

    return "Volume unmuted."

def capture_screenshot():
    try:
        screenshot_dir = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "JARVIS Screenshots"
        )

        os.makedirs(screenshot_dir, exist_ok=True)

        filename = datetime.now().strftime(
            "screenshot_%Y%m%d_%H%M%S.png"
        )

        screenshot_path = os.path.join(
            screenshot_dir,
            filename
        )

        pyautogui.screenshot(screenshot_path)

        return (
            f"Screenshot captured successfully. "
            f"Saved as {filename}."
        )

    except Exception as e:
        print(f"Screenshot error: {e}")

        return "Sorry, I could not capture the screenshot."

def read_clipboard():
    try:
        text = pyperclip.paste()

        if not text:
            return "Your clipboard is empty."

        return f"Your clipboard contains: {text}"

    except Exception as e:
        print(f"Clipboard read error: {e}")
        return "Sorry, I could not read the clipboard."


def copy_to_clipboard(text):
    try:
        if not text.strip():
            return "Please tell me what to copy."

        pyperclip.copy(text)

        return "Copied to clipboard successfully."

    except Exception as e:
        print(f"Clipboard copy error: {e}")
        return "Sorry, I could not copy the text."


def clear_clipboard():
    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Set-Clipboard -Value $null"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        return "Clipboard cleared successfully."

    except Exception as e:
        print(f"Clipboard clear error: {e}")
        return "Sorry, I could not clear the clipboard."


def internet_speed_test():

    try:

        print("🌐 Testing internet speed... Please wait.")

        st = speedtest.Speedtest()

        st.get_best_server()

        download_speed = st.download()
        upload_speed = st.upload()

        download_mbps = round(
            download_speed / 1_000_000,
            2
        )

        upload_mbps = round(
            upload_speed / 1_000_000,
            2
        )

        ping = float(
            st.results.ping
        )

        # speedtest normally returns milliseconds.
        # Reject obviously invalid values instead of
        # displaying something like 1,800,000 ms.
        if ping < 0 or ping > 1000:

            ping_text = "Unavailable"

        else:

            ping_text = f"{round(ping)} ms"

        return (
            "Internet speed test completed. "
            f"Download: {download_mbps} Mbps, "
            f"Upload: {upload_mbps} Mbps, "
            f"Ping: {ping_text}."
        )

    except Exception as e:

        print(
            f"Internet speed test error: {e}"
        )

        return (
            "Sorry, I could not complete "
            "the internet speed test. "
            "Please check your internet connection."
        )