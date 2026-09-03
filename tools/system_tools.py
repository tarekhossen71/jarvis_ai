from ctypes import POINTER, cast
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, CoCreateInstance
from datetime import datetime
import subprocess
import psutil
import shutil




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