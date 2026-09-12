
import psutil


class SystemMonitor:

    # =========================
    # Full System Status
    # =========================

    def get_status(self):

        cpu = self.get_cpu_value()
        ram = self.get_ram_value()
        disk = self.get_disk_value()
        battery = self.get_battery_value()

        return (
            f"CPU usage is {cpu}%. "
            f"Memory usage is {ram}%. "
            f"Disk usage is {disk}%. "
            f"Battery is {battery}."
        )

    # =========================
    # CPU
    # =========================

    def get_cpu_value(self):

        return psutil.cpu_percent(interval=1)

    def get_cpu(self):

        cpu = self.get_cpu_value()

        return f"CPU usage is {cpu}%."

    # =========================
    # RAM
    # =========================

    def get_ram_value(self):

        memory = psutil.virtual_memory()

        return memory.percent

    def get_ram(self):

        ram = self.get_ram_value()

        return f"Memory usage is {ram}%."

    # =========================
    # Disk
    # =========================

    def get_disk_value(self):

        disk = psutil.disk_usage("C:\\")

        return disk.percent

    def get_disk(self):

        disk = self.get_disk_value()

        return f"Disk usage is {disk}%."

    # =========================
    # Battery
    # =========================

    def get_battery_value(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return "not available"

        battery_text = f"{battery.percent}%"

        if battery.power_plugged:
            battery_text += " and currently charging"

        return battery_text

    def get_battery(self):

        battery = self.get_battery_value()

        return f"Battery is {battery}."

