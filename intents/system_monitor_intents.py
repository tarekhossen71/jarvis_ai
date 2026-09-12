
class SystemMonitorIntents:

    def __init__(self, system_monitor):
        self.system_monitor = system_monitor

    def normalize(self, text):
        return text.lower().strip()

    def execute(self, command):

        command = self.normalize(command)

        # =========================
        # Full System Status
        # =========================

        if command in [
            "how is my computer",
            "system status",
            "computer status",
            "check system",
            "check my computer",
            "system information",
            "computer information",

            # Banglish
            "amar computer kemon",
            "computer kemon ache",
            "system kemon ache",
            "amar system kemon",
        ]:

            return self.system_monitor.get_status()

        # =========================
        # CPU
        # =========================

        if command in [
            "check cpu",
            "cpu usage",
            "cpu status",
            "how is my cpu",

            # Banglish
            "cpu koto",
            "cpu usage koto",
            "cpu kemon",
        ]:

            return self.system_monitor.get_cpu()

        # =========================
        # RAM
        # =========================

        if command in [
            "check ram",
            "ram usage",
            "ram status",
            "how is my ram",
            "memory usage",

            # Banglish
            "ram koto",
            "ram usage koto",
            "ram kemon",
        ]:

            return self.system_monitor.get_ram()

        # =========================
        # Disk
        # =========================

        if command in [
            "check disk",
            "disk usage",
            "disk status",
            "how is my disk",
            "storage status",

            # Banglish
            "disk koto",
            "disk usage koto",
            "storage koto",
        ]:

            return self.system_monitor.get_disk()

        # =========================
        # Battery
        # =========================

        if command in [
            "check battery",
            "battery status",
            "how is my battery",
            "battery percentage",

            # Banglish
            "battery koto",
            "battery percentage koto",
            "battery kemon",
        ]:

            return self.system_monitor.get_battery()
            

        return None

