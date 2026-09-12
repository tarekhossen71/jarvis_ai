import re
from tools.system_tools import ( get_time, get_date, lock_pc, shutdown_pc, restart_pc, get_battery_status, get_cpu_usage, get_ram_usage, get_disk_space, get_internet_status, get_volume, set_volume, increase_volume, decrease_volume, mute_volume, unmute_volume, capture_screenshot, read_clipboard, copy_to_clipboard, clear_clipboard, internet_speed_test, )


class SystemIntents:

    def __init__(self, confirmation):
        self.confirmation = confirmation

    # =========================
    # Time
    # =========================

    def time(self, command):

        if command in [
            "time",
            "what time",
            "current time",
            "kota baje",
            "koita baje",
            "কয়টা বাজে",
            "কটা বাজে",
        ]:
            return get_time()

        return None

    # =========================
    # Date
    # =========================

    def date(self, command):

        if command in [
            "date",
            "today date",
            "current date",
            "ajker date",
            "ajke koto tarikh",
            "আজকের তারিখ",
            "আজ কত তারিখ",
        ]:
            return get_date()

        return None

    # =========================
    # Lock PC
    # =========================

    def lock(self, command):

        if command in [
            "lock pc",
            "lock computer",
            "lock my pc",
            "pc lock koro",
            "কম্পিউটার লক",
            "পিসি লক",
        ]:
            return lock_pc()

        return None

    # =========================
    # Shutdown
    # =========================

    def shutdown(self, text):

        text = self.normalize(text)

        commands = [
            "shutdown pc",
            "shutdown computer",
            "turn off pc",
            "turn off computer",
            "pc shutdown",
            "কম্পিউটার বন্ধ করো",
        ]

        if text in commands:

            return self.confirmation.ask(
                "shut down your PC",
                shutdown_pc
            )

        return None

    def restart(self, text):

        text = self.normalize(text)

        commands = [
            "restart pc",
            "restart computer",
            "reboot pc",
            "reboot computer",
            "pc restart",
            "কম্পিউটার রিস্টার্ট করো",
        ]

        if text in commands:

            return self.confirmation.ask(
                "restart your PC",
                restart_pc
            )

        return None

    
    # =========================
    # Battery
    # =========================

    def battery(self, command):

        if command in [
            "battery",
            "battery percentage",
            "battery status",
            "how much battery",
            "চার্জ কত",
            "ব্যাটারি কত",
        ]:
            return get_battery_status()

        return None

    # =========================
    # CPU
    # =========================

    def cpu(self, command):

        if command in [
            "cpu usage",
            "cpu status",
            "processor usage",
            "সিপিইউ কত",
        ]:
            return get_cpu_usage()

        return None

    # =========================
    # RAM
    # =========================

    def ram(self, command):

        if command in [
            "ram usage",
            "memory usage",
            "ram status",
            "র‍্যাম কত",
            "মেমোরি কত",
        ]:
            return get_ram_usage()

        return None

    # =========================
    # Disk
    # =========================

    def disk(self, command):

        if command in [
            "disk space",
            "disk usage",
            "c drive space",
            "hard disk space",
            "ডিস্ক স্পেস",
        ]:
            return get_disk_space()

        return None

    # =========================
    # Internet
    # =========================

    def internet(self, command):

        if command in [
            "internet status",
            "internet connection",
            "is internet working",
            "ইন্টারনেট চলছে",
            "ইন্টারনেট কানেকশন",
        ]:
            return get_internet_status()

        return None

    # =========================
    # Volume
    # =========================

    def volume(self, command):

        if command in [
            "what is the volume",
            "check volume",
            "get volume",
            "volume status",
            "আমার ভলিউম কত",
        ]:
            return get_volume()

        if command in [
            "increase volume",
            "volume up",
            "turn up volume",
            "ভলিউম বাড়াও",
        ]:
            return increase_volume()

        if command in [
            "decrease volume",
            "volume down",
            "turn down volume",
            "ভলিউম কমাও",
        ]:
            return decrease_volume()

        if command in [
            "mute volume",
            "mute",
            "ভলিউম বন্ধ করো",
        ]:
            return mute_volume()

        if command in [
            "unmute volume",
            "unmute",
            "ভলিউম চালু করো",
        ]:
            return unmute_volume()

        if command.startswith("set volume "):

            level = command.replace(
                "set volume ",
                "",
                1
            ).replace("%", "").strip()

            if level.isdigit():
                return set_volume(level)

            return "Please provide a valid volume level."

        if command.startswith("volume "):

            level = command.replace(
                "volume ",
                "",
                1
            ).replace("%", "").strip()

            if level.isdigit():
                return set_volume(level)

        return None

    # =========================
    # Screenshot
    # =========================

    def screenshot(self, command):

        if command in [
            "take a screenshot",
            "capture screenshot",
            "capture my screen",
            "take screenshot",
            "save screenshot",
            "screenshot",
            "স্ক্রিনশট নাও",
            "স্ক্রিনশট",
        ]:
            return capture_screenshot()

        return None

    # =========================
    # Clipboard
    # =========================

    def clipboard(self, command):

        if command in [
            "read clipboard",
            "what is in my clipboard",
            "show clipboard",
            "read my clipboard",
            "ক্লিপবোর্ড পড়ো",
            "ক্লিপবোর্ডে কি আছে",
        ]:
            return read_clipboard()

        if command.startswith("copy to clipboard "):

            text_to_copy = command.replace(
                "copy to clipboard ",
                "",
                1
            ).strip()

            if text_to_copy:
                return copy_to_clipboard(text_to_copy)

            return "What should I copy?"

        if command.startswith("copy "):

            text_to_copy = command[5:].strip()

            if text_to_copy:
                return copy_to_clipboard(text_to_copy)

            return "What should I copy?"

        if command in [
            "clear clipboard",
            "empty clipboard",
            "delete clipboard",
            "remove clipboard",
            "clear my clipboard",
            "ক্লিপবোর্ড পরিষ্কার করো",
            "ক্লিপবোর্ড খালি করো",
        ]:
            return clear_clipboard()

        return None

    # =========================
    # Internet Speed Test
    # =========================

    def internet_speed(self, command):

        if command in [
            "internet speed test",
            "check my internet speed",
            "check internet speed",
            "test internet speed",
            "test download speed",
            "test upload speed",
            "speed test",
            "ইন্টারনেট স্পিড টেস্ট",
            "ইন্টারনেটের স্পিড চেক করো",
        ]:
            return internet_speed_test()

        return None

    def normalize(self, text):
    
            text = text.lower().strip()
    
            # Remove common polite words
            words_to_remove = [
                "please",
                "pls",
                "plz",
                "can you",
                "could you",
                "would you",
                "would you please",
                "jarvis",
                "ভাই",
                "প্লিজ",
                "দয়া করে",
            ]
    
            for word in words_to_remove:
    
                text = text.replace(word, " ")
    
            # Remove extra spaces
            text = re.sub(r"\s+", " ", text)
    
            return text.strip()