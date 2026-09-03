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