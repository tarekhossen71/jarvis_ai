
import re
import os
from core.memory import MemoryManager
from core.confirmation import ConfirmationManager

from intents.memory_intents import MemoryIntents
from intents.help_intents import HelpIntents
from intents.reminder_intents import ReminderIntents
from intents.file_intents import FileIntents
from intents.browser_intents import BrowserIntents
from intents.system_intents import SystemIntents
from intents.camera_intents import CameraIntents
from intents.communication_intents import CommunicationIntents
from intents.automation_intents import AutomationIntents
from intents.app_intents import AppIntents
from intents.multi_step_intents import MultiStepIntents
from intents.system_monitor_intents import SystemMonitorIntents

import tools.camera_tools as camera_tools
import tools.communication_tools as communication_tools
import tools.file_tools as file_tools

from core.plugin_manager import PluginManager
from core.system_monitor import SystemMonitor
from core.reminder import ReminderManager


class IntentManager:

    def __init__(self, speaker=None, brain=None):

        self.brain = brain

        self.memory = MemoryManager()
        self.confirmation = ConfirmationManager()
        self.reminder = ReminderManager(speaker)

        # =========================
        # System Monitor
        # =========================

        self.system_monitor = SystemMonitor()

        self.system_monitor_intents = SystemMonitorIntents(
            self.system_monitor
        )

        # =========================
        # System
        # =========================

        self.system_intents = SystemIntents(
            self.confirmation
        )

        # =========================
        # Memory
        # =========================

        self.memory_intents = MemoryIntents(
            self.memory
        )

        # =========================
        # Help
        # =========================

        self.help_intents = HelpIntents(
            self.normalize
        )

        # =========================
        # Reminder
        # =========================

        self.reminder_intents = ReminderIntents(
            self.reminder
        )

        # =========================
        # Files
        # =========================

        self.file_intents = FileIntents(
            self.confirmation,
            file_tools,
            self.resolve_location
        )

        # =========================
        # Browser
        # =========================

        self.browser_intents = BrowserIntents()

        # =========================
        # Camera
        # =========================

        self.camera_intents = CameraIntents(
            camera_tools
        )

        # =========================
        # Communication
        # =========================

        self.communication_intents = CommunicationIntents(
            communication_tools,
            self.confirmation
        )

        # =========================
        # Automation
        # =========================

        self.automation_intents = AutomationIntents()

        # =========================
        # Applications
        # =========================

        self.app_intents = AppIntents()

        # =========================
        # Multi Step
        # =========================

        self.multi_step_intents = MultiStepIntents(
            self
        )

        # =========================
        # Plugins
        # =========================

        self.plugin_manager = PluginManager()

    # =========================================================
    # NORMALIZE
    # =========================================================

    def normalize(self, text):

        if not text:
            return ""

        text = str(text).lower().strip()

        # Remove punctuation from beginning/end
        text = re.sub(
            r"^[\s?!.,]+|[\s?!.,]+$",
            "",
            text
        )

        # Common polite / assistant words
        words_to_remove = [
            "would you please",
            "could you please",
            "can you please",
            "would you",
            "could you",
            "can you",
            "please",
            "pls",
            "plz",
            "jarvis",
            "ভাই",
            "প্লিজ",
            "দয়া করে",
        ]

        words_to_remove.sort(
            key=len,
            reverse=True
        )

        for word in words_to_remove:

            pattern = (
                r"(?<!\w)"
                + re.escape(word)
                + r"(?!\w)"
            )

            text = re.sub(
                pattern,
                " ",
                text,
                flags=re.IGNORECASE
            )

        # Common Banglish phrases
        # IMPORTANT:
        # Handle complete commands first.
        # This prevents:
        # "open my downloads folder"
        # from becoming:
        # "open open downloads"

        replacements = {

            # =====================================================
            # ENGLISH - COMPLETE FOLDER COMMANDS
            # =====================================================

            "open my downloads folder": "open downloads",
            "open my download folder": "open downloads",

            "open my desktop folder": "open desktop",
            "open my documents folder": "open documents",
            "open my document folder": "open documents",

            "open my pictures folder": "open pictures",
            "open my picture folder": "open pictures",

            "open my music folder": "open music",

            "open my videos folder": "open videos",
            "open my video folder": "open videos",

            # =====================================================
            # ENGLISH - WITHOUT "MY"
            # =====================================================

            "open download folder": "open downloads",
            "open downloads folder": "open downloads",

            "open desktop folder": "open desktop",

            "open document folder": "open documents",
            "open documents folder": "open documents",

            "open picture folder": "open pictures",
            "open pictures folder": "open pictures",

            "open music folder": "open music",

            "open video folder": "open videos",
            "open videos folder": "open videos",

            # =====================================================
            # SHORT ENGLISH PHRASES
            # =====================================================

            "download folder": "open downloads",
            "downloads folder": "open downloads",

            "desktop folder": "open desktop",

            "document folder": "open documents",
            "documents folder": "open documents",

            "picture folder": "open pictures",
            "pictures folder": "open pictures",

            "music folder": "open music",

            "video folder": "open videos",
            "videos folder": "open videos",

            # =====================================================
            # BANGLISH - DOWNLOADS
            # =====================================================

            "amar downloads folder open koro": "open downloads",
            "amar download folder open koro": "open downloads",
            "amar downloads open koro": "open downloads",
            "amar download open koro": "open downloads",

            # =====================================================
            # BANGLISH - DESKTOP
            # =====================================================

            "amar desktop folder open koro": "open desktop",
            "amar desktop open koro": "open desktop",

            # =====================================================
            # BANGLISH - DOCUMENTS
            # =====================================================

            "amar documents folder open koro": "open documents",
            "amar document folder open koro": "open documents",
            "amar documents open koro": "open documents",
            "amar document open koro": "open documents",

            # =====================================================
            # BANGLISH - PICTURES
            # =====================================================

            "amar pictures folder open koro": "open pictures",
            "amar picture folder open koro": "open pictures",
            "amar pictures open koro": "open pictures",
            "amar picture open koro": "open pictures",

            # =====================================================
            # BANGLISH - MUSIC
            # =====================================================

            "amar music folder open koro": "open music",
            "amar music open koro": "open music",

            # =====================================================
            # BANGLISH - VIDEOS
            # =====================================================

            "amar videos folder open koro": "open videos",
            "amar video folder open koro": "open videos",
            "amar videos open koro": "open videos",
            "amar video open koro": "open videos",

            # =====================================================
            # COMMON WEBSITE WORDING
            # =====================================================

            "go to website": "open website",
            "go to site": "open website",
            "visit site": "open website",
            "visit website": "open website",
        }

        # Longer phrases must be processed first.
        # This prevents partial replacements.
        for old, new in sorted(
            replacements.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):

            if text == old:

                text = new
                break

            text = re.sub(
                r"\b" + re.escape(old) + r"\b",
                new,
                text,
                flags=re.IGNORECASE
            )
        return text


    # =========================================================
    # WEBSITE DETECTOR
    # =========================================================

    def looks_like_website(self, command):

        if not command:
            return False

        command = command.lower().strip()

        # Explicit website commands
        explicit_patterns = [
            r"^open\s+.+\.(com|net|org|io|dev|bd|co|me|tv)(/.*)?$",
            r"^go\s+to\s+.+\.(com|net|org|io|dev|bd|co|me|tv)(/.*)?$",
            r"^visit\s+.+\.(com|net|org|io|dev|bd|co|me|tv)(/.*)?$",
            r"^open\s+https?://",
            r"^go\s+to\s+https?://",
            r"^visit\s+https?://",
        ]

        for pattern in explicit_patterns:

            if re.search(
                pattern,
                command,
                re.IGNORECASE
            ):
                return True

        return False

    # =========================================================
    # WEBSITE DIRECT EXECUTION
    # =========================================================

    def execute_website_command(self, command):

        if not command:
            return None

        command = command.strip()

        url = None

        # open facebook.com
        match = re.match(
            r"^(?:open|visit|go\s+to)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            url = match.group(1).strip()

        if not url:
            return None

        # Remove common trailing words
        url = re.sub(
            r"\s+(please|now)$",
            "",
            url,
            flags=re.IGNORECASE
        ).strip()

        # If already URL
        if not re.match(
            r"^https?://",
            url,
            re.IGNORECASE
        ):

            url = "https://" + url

        return self.browser_intents.execute(
            f"open website {url}"
        )


    def resolve_location(self, location):
        """
        Dynamically resolve a natural-language location.

        Resolution order:
        1. Real filesystem path
        2. JARVIS memory
        3. Known Windows folders
        4. Project-folder discovery
        5. Search inside likely parent folders
        """

        if not location:
            return None

        location = str(location).strip()

        # Remove trailing punctuation
        location = location.rstrip(".,!?;:")

        if not location:
            return None

        # =====================================================
        # 1. ALREADY A REAL PATH
        # =====================================================

        if (
            ":" in location
            or location.startswith("\\")
            or location.startswith("/")
        ):
            return os.path.normpath(location)

        original_location = location

        # Remove "my"
        lookup_key = re.sub(
            r"^my\s+",
            "",
            location,
            flags=re.IGNORECASE
        ).strip()

        lookup_lower = lookup_key.lower()

        # =====================================================
        # 2. MEMORY
        # =====================================================

        memory_result = self.memory.process(
            f"what is my {lookup_key}"
        )

        if memory_result:

            memory_text = str(memory_result)

            # Path inside backticks
            match = re.search(
                r"`([A-Za-z]:\\[^`]+)`",
                memory_text
            )

            if match:

                path = match.group(1).rstrip(
                    ".,!?;:"
                )

                if os.path.exists(path):
                    return os.path.normpath(path)

            # Normal Windows path
            match = re.search(
                r"([A-Za-z]:\\[^\s`]+)",
                memory_text
            )

            if match:

                path = match.group(1).rstrip(
                    ".,!?;:"
                )

                if os.path.exists(path):
                    return os.path.normpath(path)

        # =====================================================
        # 3. WINDOWS SPECIAL FOLDERS
        # =====================================================

        home = os.path.expanduser("~")

        special_folders = {

            "desktop": os.path.join(
                home,
                "Desktop"
            ),

            "downloads": os.path.join(
                home,
                "Downloads"
            ),

            "download": os.path.join(
                home,
                "Downloads"
            ),

            "documents": os.path.join(
                home,
                "Documents"
            ),

            "document": os.path.join(
                home,
                "Documents"
            ),

            "pictures": os.path.join(
                home,
                "Pictures"
            ),

            "picture": os.path.join(
                home,
                "Pictures"
            ),

            "music": os.path.join(
                home,
                "Music"
            ),

            "videos": os.path.join(
                home,
                "Videos"
            ),

            "video": os.path.join(
                home,
                "Videos"
            ),
        }

        if lookup_lower in special_folders:

            path = special_folders[
                lookup_lower
            ]

            if os.path.exists(path):
                return os.path.normpath(path)

        # =====================================================
        # 4. PROJECT FOLDER FROM MEMORY
        # =====================================================

        project_folder = None

        project_memory = self.memory.process(
            "what is my project folder"
        )

        if project_memory:

            project_text = str(
                project_memory
            )

            match = re.search(
                r"`([A-Za-z]:\\[^`]+)`",
                project_text
            )

            if match:
                project_folder = (
                    match.group(1)
                    .rstrip(".,!?;:")
                )

            else:

                match = re.search(
                    r"([A-Za-z]:\\[^\s`]+)",
                    project_text
                )

                if match:
                    project_folder = (
                        match.group(1)
                        .rstrip(".,!?;:")
                    )

        

        # =====================================================
        # 6. DYNAMIC SEARCH INSIDE PROJECT FOLDER
        # =====================================================

        if project_folder and os.path.isdir(
            project_folder
        ):

            # Search by folder name
            # Example:
            # "laravel project"
            # "crm project"
            # "jarvis project"

            search_words = re.findall(
                r"[a-z0-9]+",
                lookup_lower
            )

            ignored_words = {
                "my",
                "project",
                "projects",
                "folder",
                "directory",
                "the",
                "inside",
                "in",
                "at",
                "to",
            }

            keywords = [
                word
                for word in search_words
                if word not in ignored_words
            ]

            # -------------------------------------------------
            # Search direct child folders
            # -------------------------------------------------

            try:

                entries = os.listdir(
                    project_folder
                )

            except (PermissionError, OSError):

                entries = []

            candidates = []

            for entry in entries:

                full_path = os.path.join(
                    project_folder,
                    entry
                )

                if not os.path.isdir(
                    full_path
                ):
                    continue

                entry_lower = entry.lower()

                score = 0

                # Exact keyword match
                for keyword in keywords:

                    if keyword in entry_lower:
                        score += 10

                # -------------------------------------------------
                # Project type detection
                # -------------------------------------------------

                # Laravel
                if "laravel" in keywords:

                    if os.path.isfile(
                        os.path.join(
                            full_path,
                            "artisan"
                        )
                    ):
                        score += 30

                    if os.path.isfile(
                        os.path.join(
                            full_path,
                            "composer.json"
                        )
                    ):
                        score += 10

                    if os.path.isdir(
                        os.path.join(
                            full_path,
                            "app"
                        )
                    ):
                        score += 10

                    if os.path.isdir(
                        os.path.join(
                            full_path,
                            "routes"
                        )
                    ):
                        score += 10

                # React
                if "react" in keywords:

                    if os.path.isfile(
                        os.path.join(
                            full_path,
                            "package.json"
                        )
                    ):
                        score += 15

                    if os.path.isdir(
                        os.path.join(
                            full_path,
                            "src"
                        )
                    ):
                        score += 10

                # Python
                if "python" in keywords:

                    python_files = [
                        "requirements.txt",
                        "pyproject.toml",
                        "setup.py",
                    ]

                    for filename in python_files:

                        if os.path.isfile(
                            os.path.join(
                                full_path,
                                filename
                            )
                        ):
                            score += 20

                if score > 0:

                    candidates.append(
                        (
                            score,
                            full_path
                        )
                    )

            # -------------------------------------------------
            # Best candidate
            # -------------------------------------------------

            if candidates:

                candidates.sort(
                    key=lambda item: item[0],
                    reverse=True
                )

                best_score, best_path = (
                    candidates[0]
                )

                return os.path.normpath(
                    best_path
                )

        # =====================================================
        # 7. DIRECT FOLDER SEARCH
        # =====================================================

        # If user says:
        #
        # "LaravelNewProject"
        #
        # search inside project folder.

        if project_folder and os.path.isdir(
            project_folder
        ):

            try:

                for entry in os.listdir(
                    project_folder
                ):

                    if entry.lower() == lookup_lower:

                        full_path = os.path.join(
                            project_folder,
                            entry
                        )

                        if os.path.exists(
                            full_path
                        ):
                            return os.path.normpath(
                                full_path
                            )

            except (PermissionError, OSError):
                pass

        # =====================================================
        # 8. NOTHING FOUND
        # =====================================================

        return original_location
    # =========================================================
    # MAIN EXECUTE
    # =========================================================

    def execute(self, command):

        command = self.normalize(command)

        if not command:
            return None

        # =====================================================
        # NATURAL LANGUAGE SYSTEM ROUTING
        # =====================================================

        # Battery
        if re.search(
            r"\b(?:what(?:'s| is)?\s+)?(?:my\s+)?battery"
            r"(?:\s+(?:level|percentage|status))?\b",
            command,
            re.IGNORECASE
        ):
            return self.system_intents.battery(
                "battery"
            )


        # CPU
        if re.search(
            r"\b(?:what(?:'s| is)?\s+)?(?:my\s+)?"
            r"(?:cpu|processor)"
            r"(?:\s+(?:usage|status))?\b",
            command,
            re.IGNORECASE
        ):
            return self.system_intents.cpu(
                "cpu usage"
            )


        # RAM
        if re.search(
            r"\b(?:what(?:'s| is)?\s+)?(?:my\s+)?"
            r"(?:ram|memory)"
            r"(?:\s+(?:usage|status))?\b",
            command,
            re.IGNORECASE
        ):
            return self.system_intents.ram(
                "ram usage"
            )


        # Disk
        if re.search(
            r"\b(?:disk|storage)"
            r"(?:\s+(?:space|usage|status))?\b",
            command,
            re.IGNORECASE
        ):
            return self.system_intents.disk(
                "disk space"
            )


        # =====================================================
        # SET VOLUME
        # =====================================================

        volume_match = re.search(
            r"\b(?:set|change)"
            r"\s+(?:the\s+)?volume"
            r"(?:\s+level)?"
            r"\s*(?:to|at|=)?"
            r"\s*(\d{1,3})"
            r"\s*%?\b",
            command,
            re.IGNORECASE
        )

        if volume_match:

            level = int(
                volume_match.group(1)
            )

            level = max(
                0,
                min(100, level)
            )

            return self.system_intents.volume(
                f"set volume {level}"
            )


        # =====================================================
        # MINIMIZE WINDOW
        # =====================================================

        if command in [
            "minimize window",
            "minimize windows",
            "minimize all windows",
        ]:

            return self.app_intents.execute(
                "minimize all windows"
            )

        # =====================================================
        # Direct website detection
        # =====================================================

        if self.looks_like_website(command):

            result = self.execute_website_command(
                command
            )

            if result:
                return result

        # =====================================================
        # Window move
        # =====================================================

        if re.fullmatch(
            r"move .+ to \d+,\s*\d+",
            command,
            re.IGNORECASE
        ):
            return self.execute_single(command)

        # =====================================================
        # Memory
        # =====================================================

        memory_result = self.memory.process(command)

        if memory_result:
            return memory_result

        # =====================================================
        # Automation
        # =====================================================

        result = self.automation_intents.execute(command)

        if result:
            return result

        # =====================================================
        # Multi-step
        # =====================================================

        result = self.multi_step_intents.execute(command)

        if result:
            return result

        # =====================================================
        # Normal execution
        # =====================================================

        return self.execute_single(command)

    # =========================================================
    # AI INTENT ALIAS
    # =========================================================

    def normalize_ai_intent(self, intent):

        if not intent:
            return "unknown"

        intent = str(intent).strip().lower()

        aliases = {

            # =========================
            # SYSTEM
            # =========================

            "computer_status": "system_status",
            "get_system_status": "system_status",
            "system_info": "system_status",
            "system_information": "system_status",
            "pc_status": "system_status",
            "computer_information": "system_status",

            # =========================
            # CPU
            # =========================

            "cpu": "cpu_usage",
            "processor_usage": "cpu_usage",
            "cpu_status": "cpu_usage",

            # =========================
            # RAM
            # =========================

            "memory_usage": "ram_usage",
            "ram": "ram_usage",
            "ram_status": "ram_usage",

            # =========================
            # DISK
            # =========================

            "storage": "disk_space",
            "disk_usage": "disk_space",
            "storage_usage": "disk_space",

            # =========================
            # INTERNET
            # =========================

            "internet": "internet_status",
            "connection_status": "internet_status",
            "internet_connection": "internet_status",
            "network_status": "internet_status",

            # =========================
            # INTERNET SPEED
            # =========================

            "speed_test": "internet_speed",
            "network_speed": "internet_speed",
            "internet_speed_test": "internet_speed",

            # =========================
            # VOLUME
            # =========================

            "get_volume": "volume_status",
            "volume_status": "volume_status",
            "volume_level": "volume_status",
            "current_volume": "volume_status",

            "volume_up": "increase_volume",
            "volume_down": "decrease_volume",

            "increase_volume_level": "increase_volume",
            "decrease_volume_level": "decrease_volume",

            "mute": "mute_volume",
            "unmute": "unmute_volume",

            "change_volume": "set_volume",
            "set_volume_level": "set_volume",

            # =========================
            # SCREENSHOT
            # =========================

            "take_screenshot": "screenshot",
            "screen_capture": "screenshot",
            "capture_screen": "screenshot",
            "capture_screenshot": "screenshot",

            # =========================
            # SEARCH
            # =========================

            "search_google": "google_search",
            "search_on_google": "google_search",
            "google": "google_search",

            "search_youtube": "youtube_search",
            "search_on_youtube": "youtube_search",
            "youtube": "youtube_search",

            # =========================
            # WEBSITE
            # =========================

            "open_url": "open_website",
            "open_site": "open_website",
            "visit_website": "open_website",
            "visit_site": "open_website",
            "go_to_website": "open_website",
            "go_to_site": "open_website",
            "website": "open_website",

            # =========================
            # WEATHER
            # =========================

            "check_weather": "weather",
            "weather_check": "weather",
            "get_weather": "weather",

            # =========================
            # NEWS
            # =========================

            "search_news": "news_search",
            "latest_news": "news_search",
            "get_news": "news_search",

            # =========================
            # REMINDER
            # =========================

            "set_reminder": "create_reminder",
            "add_reminder": "create_reminder",
            "make_reminder": "create_reminder",

            "show_reminders": "list_reminders",
            "get_reminders": "list_reminders",
            "view_reminders": "list_reminders",

            "remove_reminder": "cancel_reminder",
            "delete_reminder": "cancel_reminder",
            "delete_reminders": "cancel_reminder",

            # =========================
            # CLIPBOARD
            # =========================

            "get_clipboard": "read_clipboard",
            "show_clipboard": "read_clipboard",
            "clipboard_read": "read_clipboard",

            "copy": "copy_to_clipboard",
            "copy_text": "copy_to_clipboard",

            "clear_clipboard": "clear_clipboard",

            # =========================
            # WINDOWS
            # =========================

            "list_windows": "open_windows",
            "show_windows": "open_windows",
            "get_windows": "open_windows",

            "active_window": "get_active_window",
            "current_window": "get_active_window",

            "minimize_all": "minimize_all_windows",
            "minimize_all_apps": "minimize_all_windows",

            "restore_all": "restore_all_windows",
            "restore_all_apps": "restore_all_windows",

            # =========================
            # APPLICATIONS
            # =========================

            "launch_application": "open_application",
            "start_application": "open_application",
            "launch_app": "open_application",
            "open_app": "open_application",
            "start_app": "open_application",

            "close_app": "close_application",
            "exit_application": "close_application",

            "minimize_app": "minimize_application",
            "maximize_app": "maximize_application",

            "switch_app": "switch_application",
            "change_app": "switch_application",

            # =========================
            # FILES
            # =========================

            "find_file": "search_file",
            "locate_file": "search_file",
            "search_for_file": "search_file",

            "get_file_info": "file_info",
            "file_details": "file_info",

            "rename": "rename_file",
            "rename_document": "rename_file",

            "move": "move_file",
            "move_document": "move_file",

            "remove_file": "delete_file",
            "delete_document": "delete_file",

            # =========================
            # FOLDER SHORTCUTS
            # =========================

            "desktop": "open_desktop",
            "open_my_desktop": "open_desktop",

            "downloads": "open_downloads",
            "download_folder": "open_downloads",

            "documents": "open_documents",
            "document_folder": "open_documents",

            "pictures": "open_pictures",
            "picture_folder": "open_pictures",

            "music": "open_music",
            "music_folder": "open_music",

            "videos": "open_videos",
            "video_folder": "open_videos",

            # =========================
            # CAMERA
            # =========================

            "camera": "open_camera",
            "start_camera": "open_camera",
            "open camera": "open_camera",
            "camera open": "open_camera",

            "photo": "take_photo",
            "capture_photo": "take_photo",
            "take_picture": "take_photo",

            # =========================
            # COMMUNICATION
            # =========================

            "whatsapp": "open_whatsapp",

            "send_whatsapp_message": "send_whatsapp",
            "whatsapp_message": "send_whatsapp",

            "email": "compose_email",
            "send_email": "compose_email",
            "write_email": "compose_email",

            # =========================
            # MEMORY
            # =========================

            "save_memory": "remember",
            "remember_this": "remember",

            "recall": "recall_memory",
            "get_memory": "show_memory",

            "delete_memory": "forget_memory",
            "remove_memory": "forget_memory",

            # =========================
            # PLUGINS
            # =========================

            "show_plugins": "list_plugins",
            "plugins": "list_plugins",

            "activate_plugin": "enable_plugin",
            "turn_on_plugin": "enable_plugin",

            "deactivate_plugin": "disable_plugin",
            "turn_off_plugin": "disable_plugin",

            "refresh_plugins": "reload_plugins",

            "refresh_plugin": "reload_plugin",

            "make_plugin": "create_plugin",

            "remove_plugin": "uninstall_plugin",

            "run_plugin": "execute_plugin",
        }

        return aliases.get(
            intent,
            intent
        )

    # =========================================================
    # PARAMETER HELPER
    # =========================================================

    def get_parameter(
        self,
        parameters,
        *keys,
        default=None
    ):

        if not isinstance(parameters, dict):
            return default

        for key in keys:

            value = parameters.get(key)

            if value is not None:

                if isinstance(value, str):

                    value = value.strip()

                if value != "":

                    return value

        return default

    # =========================================================
    # AI INTENT EXECUTOR
    # =========================================================

    def execute_ai_intent(self, ai_result):

        if not ai_result:
            return None

        intent = self.normalize_ai_intent(
            ai_result.get(
                "intent",
                "unknown"
            )
        )

        parameters = ai_result.get(
            "parameters",
            {}
        )
        

        if not isinstance(parameters, dict):
            parameters = {}

        action = ai_result.get(
            "action"
        )

        if not action and isinstance(parameters, dict):
            action = self.get_parameter(
                parameters,
                "action",
                "operation",
                "task"
            )
        # =====================================================
        # CLIPBOARD
        # =====================================================

        if intent == "read_clipboard":

            return self.system_intents.clipboard(
                "read clipboard"
            )

        if intent == "copy_to_clipboard":

            text = self.get_parameter(
                parameters,
                "text",
                "content",
                "value"
            )

            if not text:
                return "What should I copy?"

            return self.system_intents.clipboard(
                f"copy {text}"
            )

        if intent == "clear_clipboard":

            return self.system_intents.clipboard(
                "clear clipboard"
            )

        # =====================================================
        # SYSTEM
        # =====================================================

        if intent == "system_status":

            return self.system_monitor_intents.execute(
                "system status"
            )

        if intent == "battery":

            return self.system_intents.battery(
                "battery"
            )

        if intent == "cpu_usage":

            return self.system_intents.cpu(
                "cpu usage"
            )

        if intent == "ram_usage":

            return self.system_intents.ram(
                "ram usage"
            )

        if intent == "disk_space":

            return self.system_intents.disk(
                "disk space"
            )

        if intent == "internet_status":

            return self.system_intents.internet(
                "internet status"
            )

        # =====================================================
        # INTERNET SPEED
        # =====================================================

        if intent == "internet_speed":

            return self.system_intents.internet_speed(
                "internet speed test"
            )

        # =====================================================
        # TIME / DATE
        # =====================================================

        if intent == "get_time":

            return self.system_intents.time(
                "current time"
            )

        if intent == "get_date":

            return self.system_intents.date(
                "current date"
            )

        # =====================================================
        # VOLUME
        # =====================================================

        if intent == "volume_status":

            return self.system_intents.volume(
                "volume status"
            )

        if intent == "increase_volume":

            return self.system_intents.volume(
                "increase volume"
            )

        if intent == "decrease_volume":

            return self.system_intents.volume(
                "decrease volume"
            )

        if intent == "mute_volume":

            return self.system_intents.volume(
                "mute volume"
            )

        if intent == "unmute_volume":

            return self.system_intents.volume(
                "unmute volume"
            )

        if intent == "set_volume":

            level = self.get_parameter(
                parameters,
                "level",
                "volume",
                "value"
            )

            try:

                level = int(level)

            except (TypeError, ValueError):

                return "Please provide a valid volume level."

            level = max(
                0,
                min(100, level)
            )

            return self.system_intents.volume(
                f"set volume {level}"
            )

        # =====================================================
        # POWER
        # =====================================================

        if intent == "lock_pc":

            return self.system_intents.lock(
                "lock pc"
            )

        if intent == "shutdown_pc":

            return self.system_intents.shutdown(
                "shutdown pc"
            )

        if intent == "restart_pc":

            return self.system_intents.restart(
                "restart pc"
            )

        # =====================================================
        # SCREENSHOT
        # =====================================================

        if intent == "screenshot":

            return self.system_intents.screenshot(
                "screenshot"
            )

        # =====================================================
        # APPLICATIONS
        # =====================================================

        if intent == "open_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            if not app:
                return "Please provide an application name."

            # -------------------------------------------------
            # First check whether this is actually a folder/path
            # -------------------------------------------------

            resolved_path = self.resolve_location(app)

            if resolved_path and os.path.exists(resolved_path):

                if os.path.isdir(resolved_path):

                    try:
                        os.startfile(resolved_path)
                        return f"Opened {resolved_path}."
                    except Exception as e:
                        return f"I found {resolved_path}, but could not open it."

                if os.path.isfile(resolved_path):

                    try:
                        os.startfile(resolved_path)
                        return f"Opened {resolved_path}."
                    except Exception:
                        return f"I found {resolved_path}, but could not open it."

            # -------------------------------------------------
            # Otherwise treat it as a real application
            # -------------------------------------------------

            return self.app_intents.open_application(
                f"open {app}"
            )


        if intent == "close_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            if not app:
                return "Please provide an application name."

            return self.app_intents.close_application(
                f"close {app}"
            )


        if intent == "minimize_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            if not app:
                return "Please provide an application name."

            return self.app_intents.minimize_application(
                f"minimize {app}"
            )


        if intent == "maximize_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            if not app:
                return "Please provide an application name."

            return self.app_intents.maximize_application(
                f"maximize {app}"
            )


        if intent == "switch_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            if not app:
                return "Please provide an application name."

            return self.app_intents.switch_to_application(
                f"switch to {app}"
            )
        # =====================================================
        # WINDOWS
        # =====================================================

        if intent == "get_active_window":

            return self.app_intents.execute(
                "active window"
            )

        if intent == "open_windows":

            return self.app_intents.open_windows(
                "open windows"
            )

        if intent == "minimize_all_windows":

            return self.app_intents.execute(
                "minimize all windows"
            )

        if intent == "restore_all_windows":

            return self.app_intents.restore_all(
                "restore all windows"
            )

        if intent == "next_window":

            return self.app_intents.window_navigation(
                "next window"
            )

        if intent == "previous_window":

            return self.app_intents.window_navigation(
                "previous window"
            )

        # =====================================================
        # MOVE APPLICATION
        # =====================================================

        if intent == "move_application":

            app = self.get_parameter(
                parameters,
                "app",
                "application",
                "name"
            )

            x = self.get_parameter(
                parameters,
                "x"
            )

            y = self.get_parameter(
                parameters,
                "y"
            )

            if not app:
                return "Please provide an application name."

            if x is None or y is None:
                return "Please provide the X and Y position."

            return self.app_intents.move_app(
                f"move {app} to {x},{y}"
            )

        # =====================================================
        # BROWSER
        # =====================================================

        if intent == "open_google":

            return self.browser_intents.execute(
                "open google"
            )

        if intent == "open_youtube":

            return self.browser_intents.execute(
                "open youtube"
            )

        if intent == "open_github":

            return self.browser_intents.execute(
                "open github"
            )

        if intent == "google_search":

            query = self.get_parameter(
                parameters,
                "query",
                "search",
                "text"
            )

            if not query:
                return "What should I search on Google?"

            return self.browser_intents.execute(
                f"search google for {query}"
            )

        if intent == "youtube_search":

            query = self.get_parameter(
                parameters,
                "query",
                "search",
                "text"
            )

            if not query:
                return "What should I search on YouTube?"

            return self.browser_intents.execute(
                f"search youtube for {query}"
            )

        if intent == "open_website":

            url = self.get_parameter(
                parameters,
                "url",
                "website",
                "site",
                "query"
            )

            if not url:
                return "Please provide a website."

            if not re.match(
                r"^https?://",
                str(url),
                re.IGNORECASE
            ):

                url = "https://" + str(url)

            return self.browser_intents.execute(
                f"open website {url}"
            )

        if intent == "weather":

            location = self.get_parameter(
                parameters,
                "location",
                "city",
                "place",
                default=""
            )
            
            if location:

                return self.browser_intents.execute(
                    f"weather in {location}"
                )

            return self.browser_intents.execute(
                "weather"
            )

        if intent == "news_search":

            query = self.get_parameter(
                parameters,
                "query",
                "topic",
                "search",
                default=""
            )

            if query:

                return self.browser_intents.execute(
                    f"latest news about {query}"
                )

            return self.browser_intents.execute(
                "latest news"
            )

        # =====================================================
        # FILES
        # =====================================================

        # =====================================================
        # FILES - DYNAMIC AI EXECUTION
        # =====================================================

        if intent in [
            "files",
            "file",
            "file_management",
            "folder_management",
        ]:

            # action = self.get_parameter(
            #     parameters,
            #     "action",
            #     "operation",
            #     "task"
            # )

            if not action:
                return "What file operation should I perform?"

            action = str(action).strip().lower()

            # -------------------------------------------------
            # CREATE FOLDER
            # -------------------------------------------------

            if action in [
                "create_folder",
                "make_folder",
                "new_folder",
            ]:

                name = self.get_parameter(
                    parameters,
                    "name",
                    "folder",
                    "folder_name"
                )

                location = self.get_parameter(
                    parameters,
                    "location",
                    "path",
                    "parent",
                    "directory"
                )

                location = self.resolve_location(location)

                if not name:
                    return "Please provide a folder name."

                # Location থাকলে সরাসরি existing tool ব্যবহার
                if location:

                    return self.file_intents.tools.create_folder(
                        name,
                        location
                    )

                return self.file_intents.tools.create_folder(name)

            # -------------------------------------------------
            # CREATE FILE
            # -------------------------------------------------

            if action in [
                "create_file",
                "make_file",
                "new_file",
            ]:

                name = self.get_parameter(
                    parameters,
                    "name",
                    "file",
                    "filename",
                    "file_name"
                )

                location = self.get_parameter(
                    parameters,
                    "location",
                    "path",
                    "directory",
                    "folder"
                )

                location = self.resolve_location(location)

                content = self.get_parameter(
                    parameters,
                    "content",
                    "text",
                    "value",
                    default=""
                )

                if not name:
                    return "Please provide a file name."

                return self.file_intents.tools.create_text_file(
                    name,
                    location,
                    content
                )

            # -------------------------------------------------
            # WRITE FILE
            # -------------------------------------------------

            if action in [
                "write_file",
                "overwrite_file",
                "replace_file_content",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "filename",
                    "file_path"
                )

                content = self.get_parameter(
                    parameters,
                    "content",
                    "text",
                    "value",
                    default=""
                )

                if not path:
                    return "Please provide the file path."
                
                path = self.resolve_location(path)

                return self.file_intents.write_file(
                    f"write {content} to {path}"
                )

            # -------------------------------------------------
            # APPEND FILE
            # -------------------------------------------------

            if action in [
                "append_file",
                "add_to_file",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "filename",
                    "file_path"
                )

                content = self.get_parameter(
                    parameters,
                    "content",
                    "text",
                    "value",
                    default=""
                )

                if not path:
                    return "Please provide the file path."

                if not content:
                    return "Please provide the content to append."

                return self.file_intents.append_file(
                    f"append {content} to {path}"
                )

            # -------------------------------------------------
            # READ FILE
            # -------------------------------------------------

            if action in [
                "read_file",
                "show_file",
                "read_content",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "filename",
                    "file_path"
                )

                if not path:
                    return "Please provide the file path."

                return self.file_intents.read_file(
                    f"read file {path}"
                )

            # -------------------------------------------------
            # SEARCH FILE
            # -------------------------------------------------

            if action in [
                "search_file",
                "find_file",
                "locate_file",
                "search_files",
            ]:

                query = self.get_parameter(
                    parameters,
                    "query",
                    "name",
                    "filename",
                    "file",
                    "search"
                )

                if not query:
                    return "What file should I search for?"

                return self.file_intents.search_file(
                    f"search file {query}"
                )

            # -------------------------------------------------
            # FILE INFO
            # -------------------------------------------------

            if action in [
                "file_info",
                "file_details",
                "get_file_info",
                "file_information",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "filename"
                )

                if not path:
                    return "Please provide the file path."

                return self.file_intents.file_info(
                    f"file info {path}"
                )

            # -------------------------------------------------
            # OPEN PATH
            # -------------------------------------------------

            if action in [
                "open_path",
                "open_file",
                "open_folder",
                "open_directory",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "folder",
                    "directory"
                )

                if not path:
                    return "Please provide the path."

                # Dynamically resolve natural-language location
                resolved_path = self.resolve_location(path)

                if not resolved_path:
                    return f"I couldn't find '{path}'."

                # Use the resolved real path
                return self.file_intents.open_path(
                    f"open path {resolved_path}"
                )

            # -------------------------------------------------
            # RECENT FILES
            # -------------------------------------------------

            if action in [
                "recent_files",
                "show_recent_files",
                "get_recent_files",
            ]:

                return self.file_intents.recent_files(
                    "recent files"
                )

            # -------------------------------------------------
            # RENAME
            # -------------------------------------------------

            if action in [
                "rename_file",
                "rename_folder",
                "rename_item",
                "rename",
            ]:

                old_name = self.get_parameter(
                    parameters,
                    "old_name",
                    "old",
                    "source",
                    "current_name"
                )

                new_name = self.get_parameter(
                    parameters,
                    "new_name",
                    "new",
                    "destination",
                    "new_filename"
                )

                if not old_name or not new_name:
                    return (
                        "Please provide both old and new names."
                    )

                return self.file_intents.rename(
                    f"rename {old_name} to {new_name}"
                )

            # -------------------------------------------------
            # MOVE
            # -------------------------------------------------

            if action in [
                "move_file",
                "move_folder",
                "move_item",
                "move",
            ]:

                source = self.get_parameter(
                    parameters,
                    "source",
                    "path",
                    "file",
                    "folder",
                    "item"
                )

                source_location = self.get_parameter(
                    parameters,
                    "source_location",
                    "source_folder",
                    "from_folder",
                    "source_directory",
                    "from_directory"
                )

                destination = self.get_parameter(
                    parameters,
                    "destination",
                    "destination_folder",
                    "dest",
                    "target",
                    "target_folder"
                )

                if not source or not destination:
                    return "Please provide source and destination."

                # Resolve source folder
                if source_location:

                    resolved_source_location = self.resolve_location(
                        source_location
                    )

                    if not resolved_source_location:
                        return (
                            f"I could not find the source folder "
                            f"'{source_location}'."
                        )

                    # If source is only a filename,
                    # combine it with source folder.
                    source_text = str(source).strip()

                    if not (
                        ":" in source_text
                        or source_text.startswith("\\")
                        or source_text.startswith("/")
                    ):
                        source = os.path.join(
                            resolved_source_location,
                            source_text
                        )

                else:
                    source = self.resolve_location(source)

                # Resolve destination folder
                destination = self.resolve_location(
                    destination
                )

                # Confirmation
                return self.confirmation.ask(
                    f"move {os.path.basename(source)} "
                    f"from {os.path.dirname(source)} "
                    f"to {destination}",
                    lambda: self.file_intents.tools.move_item(
                        source,
                        destination
                    )
                )

            # -------------------------------------------------
            # DELETE
            # -------------------------------------------------

            if action in [
                "delete_file",
                "delete_folder",
                "delete_item",
                "remove_file",
                "remove_folder",
                "delete",
            ]:

                path = self.get_parameter(
                    parameters,
                    "path",
                    "file",
                    "folder",
                    "filename",
                    "item"
                )

                if not path:
                    return "What should I delete?"

                return self.file_intents.delete(
                    f"delete {path}"
                )

            # -------------------------------------------------
            # EMPTY RECYCLE BIN
            # -------------------------------------------------

            if action in [
                "empty_recycle_bin",
                "clear_recycle_bin",
                "empty_trash",
            ]:

                return self.file_intents.empty_recycle_bin(
                    "empty recycle bin"
                )

            return (
                f"I don't know how to perform the file "
                f"operation '{action}'."
            )

        # =====================================================
        # FOLDER SHORTCUTS
        # =====================================================

        if intent == "open_desktop":

            return self.file_intents.desktop(
                "open desktop"
            )

        if intent == "open_downloads":

            return self.file_intents.downloads(
                "open downloads"
            )

        if intent == "open_documents":

            return self.file_intents.documents(
                "open documents"
            )

        if intent == "open_pictures":

            return self.file_intents.pictures(
                "open pictures"
            )

        if intent == "open_music":

            return self.file_intents.music(
                "open music"
            )

        if intent == "open_videos":

            return self.file_intents.videos(
                "open videos"
            )

        # =====================================================
        # REMINDER
        # =====================================================

        if intent == "create_reminder":

            text = self.get_parameter(
                parameters,
                "text",
                "message",
                "reminder"
            )

            reminder_time = self.get_parameter(
                parameters,
                "time",
                "datetime",
                "date_time"
            )

            if not text:
                return "What should I remind you about?"

            if not reminder_time:
                return "When should I remind you?"

            return self.reminder_intents.create_reminder(
                f"remind me to {text} at {reminder_time}"
            )

        if intent == "list_reminders":

            return self.reminder_intents.list_reminders(
                "list reminders"
            )

        if intent == "cancel_reminder":

            reminder_id = self.get_parameter(
                parameters,
                "id",
                "reminder_id"
            )

            if reminder_id:

                return self.reminder_intents.cancel_reminder(
                    f"cancel reminder {reminder_id}"
                )

            return self.reminder_intents.cancel_reminder(
                "cancel reminder"
            )

        # =====================================================
        # CAMERA
        # =====================================================

        if intent == "open_camera":

            return self.camera_intents.execute(
                "open camera"
            )

        if intent == "close_camera":

            return self.camera_intents.execute(
                "close camera"
            )

        if intent == "take_photo":

            return self.camera_intents.execute(
                "take photo"
            )

        if intent == "camera_status":

            return self.camera_intents.execute(
                "camera status"
            )

        if intent == "live_preview":

            return self.camera_intents.execute(
                "live preview"
            )

        if intent == "stop_preview":

            return self.camera_intents.execute(
                "stop preview"
            )

        # =====================================================
        # COMMUNICATION
        # =====================================================

        if intent == "open_whatsapp":

            return self.communication_intents.execute(
                "open whatsapp"
            )

        if intent == "send_whatsapp":

            recipient = self.get_parameter(
                parameters,
                "recipient",
                "contact",
                "person",
                "to"
            )

            message = self.get_parameter(
                parameters,
                "message",
                "text",
                "body"
            )

            if not recipient:
                return (
                    "Who should I send the WhatsApp message to?"
                )

            if not message:
                return "What message should I send?"

            return self.communication_intents.execute(
                f"send whatsapp to {recipient} {message}"
            )

        if intent == "open_email":

            return self.communication_intents.execute(
                "open email"
            )

        if intent == "compose_email":

            recipient = self.get_parameter(
                parameters,
                "recipient",
                "email",
                "to",
                default=""
            )

            subject = self.get_parameter(
                parameters,
                "subject",
                "title",
                default=""
            )

            body = self.get_parameter(
                parameters,
                "body",
                "message",
                "text",
                default=""
            )

            command_parts = [
                "compose email"
            ]

            if recipient:
                command_parts.append(
                    f"to {recipient}"
                )

            if subject:
                command_parts.append(
                    f"subject {subject}"
                )

            if body:
                command_parts.append(
                    f"body {body}"
                )

            return self.communication_intents.execute(
                " ".join(command_parts)
            )

        # =====================================================
        # MEMORY
        # =====================================================

        if intent == "remember":

            key = self.get_parameter(
                parameters,
                "key",
                "name"
            )

            value = self.get_parameter(
                parameters,
                "value",
                "content"
            )

            if key and value:

                return self.memory.process(
                    f"remember my {key} is {value}"
                )

            text = self.get_parameter(
                parameters,
                "text",
                "message"
            )

            if text:

                return self.memory.process(
                    f"remember {text}"
                )

            return "What should I remember?"

        if intent == "recall_memory":

            key = self.get_parameter(
                parameters,
                "key",
                "name"
            )

            if key:

                return self.memory.process(
                    f"what is my {key}"
                )

            return self.memory.process(
                "show memory"
            )

        if intent == "show_memory":

            return self.memory.process(
                "show memory"
            )

        if intent == "forget_memory":

            key = self.get_parameter(
                parameters,
                "key",
                "name",
                "memory"
            )

            if not key:
                return "What should I forget?"

            return self.memory.process(
                f"forget {key}"
            )

        # =====================================================
        # PLUGINS
        # =====================================================

        if intent == "list_plugins":

            plugins = self.plugin_manager.get_plugin_details()

            if not plugins:
                return "No plugins are currently loaded."

            result = "Loaded plugins:\n"

            for index, plugin in enumerate(
                plugins,
                start=1
            ):

                status = (
                    "Enabled"
                    if plugin["enabled"]
                    else "Disabled"
                )

                result += (
                    f"{index}. "
                    f"{plugin['name']} "
                    f"({status})\n"
                )

            return result.strip()

        if intent == "enable_plugin":

            name = self.get_parameter(
                parameters,
                "name",
                "plugin",
                "plugin_name"
            )

            if not name:
                return "Please provide a plugin name."

            return self.plugin_manager.enable_plugin(
                name
            )

        if intent == "disable_plugin":

            name = self.get_parameter(
                parameters,
                "name",
                "plugin",
                "plugin_name"
            )

            if not name:
                return "Please provide a plugin name."

            return self.plugin_manager.disable_plugin(
                name
            )

        if intent == "reload_plugins":

            return self.plugin_manager.reload_plugins()

        if intent == "reload_plugin":

            name = self.get_parameter(
                parameters,
                "name",
                "plugin",
                "plugin_name"
            )

            if not name:
                return "Please provide a plugin name."

            return self.plugin_manager.reload_plugin(
                name
            )

        if intent == "create_plugin":

            name = self.get_parameter(
                parameters,
                "name",
                "plugin",
                "plugin_name"
            )

            if not name:
                return "Please provide a plugin name."

            return self.plugin_manager.create_plugin(
                name
            )

        if intent == "uninstall_plugin":

            name = self.get_parameter(
                parameters,
                "name",
                "plugin",
                "plugin_name"
            )

            if not name:
                return "Please provide a plugin name."

            plugin = self.plugin_manager.find_plugin(
                name
            )

            if not plugin:
                return (
                    f"Plugin '{name}' was not found."
                )

            return self.confirmation.ask(
                f"uninstall {plugin['name']}",
                lambda: self.plugin_manager.delete_plugin(
                    plugin["name"]
                )
            )

        if intent == "execute_plugin":

            command_text = self.get_parameter(
                parameters,
                "command",
                "text",
                "query"
            )

            if not command_text:
                return "What plugin command should I run?"

            return self.plugin_manager.execute(
                command_text
            )

        # =====================================================
        # UNKNOWN
        # =====================================================

        return None

    # =========================================================
    # NORMAL / STATIC COMMAND EXECUTION
    # =========================================================

    def execute_single(self, command):

        command = self.normalize(command)

        if not command:
            return None

        # =====================================================
        # CONFIRMATION
        # =====================================================

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

        # =====================================================
        # RELOAD JARVIS
        # =====================================================

        if command in [
            "reload jarvis",
            "reload",
        ]:
            return "__RELOAD_JARVIS__"

        # =====================================================
        # WEBSITE - BEFORE APPLICATION
        # =====================================================

        if self.looks_like_website(command):

            result = self.execute_website_command(
                command
            )

            if result:
                return result

        # =====================================================
        # MEMORY
        # =====================================================

        memory_result = self.memory.process(
            command
        )

        if memory_result:
            return memory_result

        # =====================================================
        # HELP
        # =====================================================

        result = self.help_intents.smart_help(
            command
        )

        if result:
            return result

        # =====================================================
        # REMINDER
        # =====================================================

        result = self.reminder_intents.create_reminder(
            command
        )

        if result:
            return result

        result = self.reminder_intents.list_reminders(
            command
        )

        if result:
            return result

        result = self.reminder_intents.cancel_reminder(
            command
        )

        if result:
            return result

        # =====================================================
        # WINDOW MOVE
        # =====================================================

        if re.fullmatch(
            r"move .+ to \d+,\s*\d+",
            command,
            re.IGNORECASE
        ):

            result = self.app_intents.move_app(
                command
            )

            if result:
                return result

        if re.fullmatch(
            r"move .+ to position \d+,\s*\d+",
            command,
            re.IGNORECASE
        ):

            result = self.app_intents.move_app(
                command
            )

            if result:
                return result
        # =====================================================
        # DIRECT FOLDER SHORTCUTS
        # =====================================================

        folder_commands = {
            "open desktop": self.file_intents.desktop,
            "open downloads": self.file_intents.downloads,
            "open download": self.file_intents.downloads,
            "open documents": self.file_intents.documents,
            "open document": self.file_intents.documents,
            "open pictures": self.file_intents.pictures,
            "open picture": self.file_intents.pictures,
            "open music": self.file_intents.music,
            "open videos": self.file_intents.videos,
            "open video": self.file_intents.videos,

            "desktop": self.file_intents.desktop,
            "downloads": self.file_intents.downloads,
            "download": self.file_intents.downloads,
            "documents": self.file_intents.documents,
            "document": self.file_intents.documents,
            "pictures": self.file_intents.pictures,
            "picture": self.file_intents.pictures,
            "music": self.file_intents.music,
            "videos": self.file_intents.videos,
            "video": self.file_intents.videos,
        }

        folder_handler = folder_commands.get(command)

        if folder_handler:

            result = folder_handler(command)

            if result:
                return result
        # =====================================================
        # FILE INTENTS - BASIC
        # =====================================================

        result = self.file_intents.create_folder(
            command
        )

        if result:
            return result

        result = self.file_intents.create_file(
            command
        )

        if result:
            return result

        result = self.file_intents.search_file(
            command
        )

        if result:
            return result

        result = self.file_intents.file_info(
            command
        )

        if result:
            return result

        result = self.file_intents.recent_files(
            command
        )

        if result:
            return result

        result = self.file_intents.open_path(
            command
        )

        if result:
            return result

        result = self.file_intents.rename(
            command
        )

        if result:
            return result

        # result = self.file_intents.move(
        #     command
        # )

        # if result:
        #     return result

        result = self.file_intents.delete(
            command
        )

        if result:
            return result

        result = self.file_intents.empty_recycle_bin(
            command
        )

        if result:
            return result

        # =====================================================
        # SYSTEM
        # =====================================================

        result = self.system_intents.time(
            command
        )

        if result:
            return result

        result = self.system_intents.date(
            command
        )

        if result:
            return result

        result = self.system_intents.lock(
            command
        )

        if result:
            return result

        result = self.system_intents.shutdown(
            command
        )

        if result:
            return result

        result = self.system_intents.restart(
            command
        )

        if result:
            return result

        # =====================================================
        # SYSTEM MONITOR
        # =====================================================

        result = self.system_monitor_intents.execute(
            command
        )

        if result:
            return result

        result = self.system_intents.battery(
            command
        )

        if result:
            return result

        result = self.system_intents.cpu(
            command
        )

        if result:
            return result

        result = self.system_intents.ram(
            command
        )

        if result:
            return result

        result = self.system_intents.disk(
            command
        )

        if result:
            return result

        result = self.system_intents.internet(
            command
        )

        if result:
            return result

        result = self.system_intents.volume(
            command
        )

        if result:
            return result

        result = self.system_intents.screenshot(
            command
        )

        if result:
            return result

        result = self.system_intents.clipboard(
            command
        )

        if result:
            return result

        result = self.system_intents.internet_speed(
            command
        )

        if result:
            return result

        # =====================================================
        # AUTOMATION
        # =====================================================

        result = self.automation_intents.execute(
            command
        )

        if result:
            return result

        # =====================================================
        # BROWSER
        # =====================================================

        result = self.browser_intents.execute(
            command
        )

        if result:
            return result


        
        # =====================================================
        # APPLICATIONS
        # =====================================================
        if command.startswith("open "):

            open_target = command[5:].strip()

            if open_target:

                resolved_path = self.resolve_location(
                    open_target
                )

                if (
                    resolved_path
                    and os.path.exists(resolved_path)
                ):

                    try:

                        os.startfile(
                            os.path.normpath(
                                resolved_path
                            )
                        )

                        return (
                            f"Opened "
                            f"{os.path.normpath(resolved_path)}."
                        )

                    except Exception as e:

                        return (
                            f"I found "
                            f"{os.path.normpath(resolved_path)}, "
                            f"but could not open it."
                        )
        result = self.app_intents.execute(
            command
        )

        if result:
            return result

        # =====================================================
        # PLUGIN MANAGEMENT
        # =====================================================

        if command in [
            "list plugins",
            "show plugins",
            "plugin list",
        ]:

            plugins = self.plugin_manager.get_plugin_details()

            if not plugins:
                return "No plugins are currently loaded."

            result = "Loaded plugins:\n"

            for index, plugin in enumerate(
                plugins,
                start=1
            ):

                status = (
                    "Enabled"
                    if plugin["enabled"]
                    else "Disabled"
                )

                result += (
                    f"{index}. "
                    f"{plugin['name']} "
                    f"({status})\n"
                )

            return result.strip()

        if command.startswith(
            "disable plugin "
        ):

            plugin_name = command.replace(
                "disable plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.disable_plugin(
                plugin_name
            )

        if command.startswith(
            "enable plugin "
        ):

            plugin_name = command.replace(
                "enable plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.enable_plugin(
                plugin_name
            )

        if command in [
            "reload plugins",
            "reload plugin",
            "refresh plugins",
            "refresh plugin",
        ]:

            return self.plugin_manager.reload_plugins()

        if command.startswith(
            "reload plugin "
        ):

            plugin_name = command.replace(
                "reload plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.reload_plugin(
                plugin_name
            )

        if command.startswith(
            "create plugin "
        ):

            plugin_name = command.replace(
                "create plugin ",
                "",
                1
            ).strip()

            return self.plugin_manager.create_plugin(
                plugin_name
            )

        if command.startswith(
            "uninstall "
        ):

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

        # =====================================================
        # EXECUTE PLUGIN
        # =====================================================

        result = self.plugin_manager.execute(
            command
        )

        if result:
            return result

        
        # =====================================================
        # FILE - ADVANCED
        # =====================================================

        result = self.file_intents.write_file(
            command
        )

        if result:
            return result

        result = self.file_intents.append_file(
            command
        )

        if result:
            return result

        result = self.file_intents.read_file(
            command
        )

        if result:
            return result

        result = self.file_intents.search_file(
            command
        )

        if result:
            return result

        result = self.file_intents.file_info(
            command
        )

        if result:
            return result

        result = self.file_intents.recent_files(
            command
        )

        if result:
            return result

        result = self.file_intents.open_path(
            command
        )

        if result:
            return result

        result = self.file_intents.rename(
            command
        )

        if result:
            return result

        # result = self.file_intents.move(
        #     command
        # )

        # if result:
        #     return result

        result = self.file_intents.delete(
            command
        )

        if result:
            return result

        result = self.file_intents.empty_recycle_bin(
            command
        )

        if result:
            return result

        # =====================================================
        # CAMERA
        # =====================================================

        result = self.camera_intents.execute(
            command
        )

        if result:
            return result

        # =====================================================
        # COMMUNICATION
        # =====================================================

        result = self.communication_intents.execute(
            command
        )

        if result:
            return result

        # =====================================================
        # AI DYNAMIC FALLBACK
        #
        # This is intentionally near the END.
        # Static handlers get first chance.
        # =====================================================

        if self.brain:

            ai_result = self.brain.classify_intent(
                command
            )

            result = self.execute_ai_intent(
                ai_result
            )

            if result:
                return result

        # =====================================================
        # NOTHING FOUND
        # =====================================================

        return None
