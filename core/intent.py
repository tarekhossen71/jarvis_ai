import re
from core.memory import MemoryManager
from core.confirmation import ConfirmationManager
from intents.memory_intents import MemoryIntents
from intents.help_intents import HelpIntents
from intents.reminder_intents import ReminderIntents
from intents.file_intents import FileIntents
from intents.browser_intents import BrowserIntents
from intents.system_intents import SystemIntents
from intents.camera_intents import CameraIntents
import tools.camera_tools as camera_tools
from intents.communication_intents import CommunicationIntents
import tools.communication_tools as communication_tools
from intents.automation_intents import AutomationIntents
from intents.app_intents import AppIntents
from intents.multi_step_intents import MultiStepIntents
from core.plugin_manager import PluginManager



from core.reminder import ReminderManager
import tools.file_tools as file_tools
class IntentManager:

    def __init__(self, speaker=None):
        self.memory = MemoryManager()
        self.confirmation = ConfirmationManager()
        self.reminder = ReminderManager(speaker)
        # =========================
        # System
        # =========================
        self.system_intents = SystemIntents(
            self.confirmation
        )

        self.memory_intents = MemoryIntents(self.memory)
        self.help_intents = HelpIntents(self.normalize)
        self.reminder_intents = ReminderIntents(self.reminder)

        self.file_intents = FileIntents(
            self.confirmation,
            file_tools
        )

        self.browser_intents = BrowserIntents()

        # Camera
        self.camera_intents = CameraIntents(camera_tools)

        # Communication
        self.communication_intents = CommunicationIntents(
            communication_tools,
            self.confirmation
        )

        # Advanced Automation
        self.automation_intents = AutomationIntents()

        self.app_intents = AppIntents()

        self.multi_step_intents = MultiStepIntents(self)

        self.plugin_manager = PluginManager()
    # =========================
    # Normalize Text
    # =========================

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

            # text = text.replace(word, " ")
            text = re.sub(r"[?!]+$", "", text)
        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()


    # Execute
    def execute(self, command):

        command = self.normalize(command)

        if not command:
            return None

        memory_result = self.memory.process(command)

        if memory_result:
            return memory_result

        # Automation
        result = self.automation_intents.execute(command)

        if result:
            return result
        
        # =========================
        # Multi-Step Automation
        # =========================

        result = self.multi_step_intents.execute(command)

        if result:
            return result

        # Other intents
        return self.execute_single(command)
    
    def execute_single(self, command):

        command = self.normalize(command)

        if not command:
            return None

       
        if self.confirmation.has_pending():

            if command in [
                "yes",
                "yes jarvis",
                "confirm",
                "do it",
                "হ্যাঁ",
                "জি",
            ]:
                return self.confirmation.confirm()

            if command in [
                "no",
                "no jarvis",
                "cancel",
                "don't",
                "না",
                "বাতিল",
            ]:
                return self.confirmation.cancel()


        
        # =========================
        # Restart JARVIS
        # =========================

        if command in [
            "reload jarvis",
            "reload",
        ]:

            return "__RELOAD_JARVIS__"
    

        # -------------------------
        # Memory
        # -------------------------
        memory_result = self.memory.process(command)

        if memory_result:
            return memory_result

        # -------------------------
        # Help
        # -------------------------
        result = self.help_intents.smart_help(command)

        if result:
            return result

        # -------------------------
        # Reminder
        # -------------------------
        result = self.reminder_intents.create_reminder(command)
        if result:
            return result

        result = self.reminder_intents.list_reminders(command)
        if result:
            return result

        result = self.reminder_intents.cancel_reminder(command)
        if result:
            return result

        # =========================
        # FILE INTENTS
        # =========================

        result = self.file_intents.create_folder(command)
        if result:
            return result

        result = self.file_intents.create_file(command)
        if result:
            return result

        result = self.file_intents.search_file(command)
        if result:
            return result

        result = self.file_intents.file_info(command)
        if result:
            return result

        result = self.file_intents.recent_files(command)
        if result:
            return result

        result = self.file_intents.open_path(command)
        if result:
            return result

        result = self.file_intents.rename(command)
        if result:
            return result

        result = self.file_intents.move(command)
        if result:
            return result

        result = self.file_intents.delete(command)
        if result:
            return result

        result = self.file_intents.empty_recycle_bin(command)
        if result:
            return result

        # =========================
        # SYSTEM INTENTS
        # =========================

        result = self.system_intents.time(command)
        if result:
            return result

        result = self.system_intents.date(command)
        if result:
            return result

        result = self.system_intents.lock(command)
        if result:
            return result

        result = self.system_intents.shutdown(command)
        if result:
            return result

        result = self.system_intents.restart(command)
        if result:
            return result

        result = self.system_intents.battery(command)
        if result:
            return result

        result = self.system_intents.cpu(command)
        if result:
            return result

        result = self.system_intents.ram(command)
        if result:
            return result

        result = self.system_intents.disk(command)
        if result:
            return result

        result = self.system_intents.internet(command)
        if result:
            return result

        result = self.system_intents.volume(command)
        if result:
            return result

        result = self.system_intents.screenshot(command)
        if result:
            return result

        result = self.system_intents.clipboard(command)
        if result:
            return result

        result = self.system_intents.internet_speed(command)
        if result:
            return result


        # =========================
        # Advanced Automation
        # =========================

        result = self.automation_intents.execute(command)

        if result:
            return result

        result = self.app_intents.execute(command)

        if result:
            return result
        
        # =========================
        # BROWSER INTENTS
        # =========================
        
        result = self.browser_intents.execute(command)

        if result:
            return result

        # =========================
        # Plugin Management
        # =========================

        # -------------------------
        # Plugin List
        # -------------------------

        if command in [
            "list plugins",
            "show plugins",
            "plugin list",
        ]:

            plugins = self.plugin_manager.get_plugin_details()

            if not plugins:
                return "No plugins are currently loaded."

            result = "Loaded plugins:\n"

            for index, plugin in enumerate(plugins, start=1):

                status = (
                    "Enabled"
                    if plugin["enabled"]
                    else "Disabled"
                )

                result += (
                    f"{index}. {plugin['name']} "
                    f"({status})\n"
                )

            return result


        # -------------------------
        # Disable Plugin
        # -------------------------

        if command.startswith("disable plugin "):

            plugin_name = command.replace(
                "disable plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.disable_plugin(
                plugin_name
            )


        if command.startswith("disable ") and "plugin" in command:

            plugin_name = command.replace(
                "disable ",
                "",
                1
            ).strip()

            return self.plugin_manager.disable_plugin(
                plugin_name
            )


        # -------------------------
        # Enable Plugin
        # -------------------------

        if command.startswith("enable plugin "):

            plugin_name = command.replace(
                "enable plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.enable_plugin(
                plugin_name
            )


        if command.startswith("enable ") and "plugin" in command:

            plugin_name = command.replace(
                "enable ",
                "",
                1
            ).strip()

            return self.plugin_manager.enable_plugin(
                plugin_name
            )


        # -------------------------
        # Reload Plugins
        # -------------------------

        if command in [
            "reload plugins",
            "reload plugin",
            "refresh plugins",
            "refresh plugin",
        ]:

            return self.plugin_manager.reload_plugins()


        # -------------------------
        # Reload Single Plugin
        # -------------------------

        if command.startswith("reload plugin "):

            plugin_name = command.replace(
                "reload plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.reload_plugin(
                plugin_name
            )


        # -------------------------
        # Create Plugin
        # -------------------------

        if command.startswith("create plugin "):

            plugin_name = command.replace(
                "create plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.create_plugin(
                plugin_name
            )


        # -------------------------
        # Uninstall Plugin
        # -------------------------

        if command.startswith("uninstall "):

            plugin_name = command.replace(
                "uninstall ",
                "",
                1
            ).strip()

            if not plugin_name:
                return "Please provide a plugin name."

            plugin = self.plugin_manager.find_plugin(
                plugin_name
            )

            if not plugin:
                return (
                    f"Plugin '{plugin_name}' "
                    f"was not found."
                )

            return self.confirmation.ask(
                f"uninstall {plugin['name']}",
                lambda: self.plugin_manager.delete_plugin(
                    plugin["name"]
                )
            )


        # =========================
        # Execute Plugin
        # =========================

        # IMPORTANT:
        # This must stay AFTER all plugin management
        # commands such as uninstall, reload, create,
        # enable and disable.

        result = self.plugin_manager.execute(command)

        if result:
            return result
        

    

        # =========================
        # File Intents
        # =========================

        result = self.file_intents.desktop(command)
        if result:
            return result

        result = self.file_intents.downloads(command)
        if result:
            return result

        result = self.file_intents.documents(command)
        if result:
            return result

        result = self.file_intents.pictures(command)
        if result:
            return result

        result = self.file_intents.music(command)
        if result:
            return result

        result = self.file_intents.videos(command)
        if result:
            return result

        result = self.file_intents.create_folder(command)
        if result:
            return result

        result = self.file_intents.create_file(command)
        if result:
            return result

        result = self.file_intents.write_file(command)
        if result:
            return result

        result = self.file_intents.append_file(command)
        if result:
            return result

        result = self.file_intents.read_file(command)
        if result:
            return result

        result = self.file_intents.search_file(command)
        if result:
            return result

        result = self.file_intents.file_info(command)
        if result:
            return result

        result = self.file_intents.recent_files(command)
        if result:
            return result

        result = self.file_intents.open_path(command)
        if result:
            return result

        result = self.file_intents.rename(command)
        if result:
            return result

        result = self.file_intents.move(command)
        if result:
            return result

        result = self.file_intents.delete(command)
        if result:
            return result

        result = self.file_intents.empty_recycle_bin(command)
        if result:
            return result


        result = self.camera_intents.execute(command)
        if result:
            return result
        



        result = self.communication_intents.execute(command)
        if result:
            return result

        
        # =========================
        # NORMAL COMMANDS
        # =========================

        # for intent, data in self.commands.items():

        #     for keyword in data["keywords"]:

        #         if keyword in command:

        #             return data["function"]()


        return None

    
