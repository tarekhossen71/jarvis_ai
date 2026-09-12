
import time
import requests
import json
import re

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_PROMPT
from core.memory import MemoryManager


class Brain:

    # ============================================================
    # VALID AI INTENTS
    # ============================================================

    VALID_INTENTS = {
        # System
        "system_status",
        "battery",
        "cpu_usage",
        "ram_usage",
        "disk_space",
        "internet_status",
        "internet_speed",

        # Time
        "get_time",
        "get_date",

        # Volume
        "get_volume",
        "increase_volume",
        "decrease_volume",
        "mute_volume",
        "unmute_volume",
        "set_volume",

        # Power
        "lock_pc",
        "shutdown_pc",
        "restart_pc",

        # Screen
        "screenshot",

        # Clipboard
        "read_clipboard",
        "copy_to_clipboard",
        "clear_clipboard",

        # Applications
        "open_application",
        "close_application",
        "minimize_application",
        "maximize_application",
        "switch_application",
        "get_active_window",
        "get_open_windows",
        "minimize_all_windows",
        "restore_all_windows",

        # Windows
        "next_window",
        "previous_window",
        "move_application",

        # Browser
        "open_google",
        "open_youtube",
        "open_github",
        "google_search",
        "youtube_search",
        "open_website",
        "weather",
        "news_search",

        # Files
        "files",
        "create_folder",
        "create_file",
        "write_file",
        "append_file",
        "read_file",
        "search_file",
        "file_info",
        "rename_file",
        "move_file",
        "delete_file",

        # Folders
        "open_desktop",
        "open_downloads",
        "open_documents",
        "open_pictures",
        "open_music",
        "open_videos",

        # Reminders
        "create_reminder",
        "list_reminders",
        "cancel_reminder",

        # Camera
        "open_camera",
        "close_camera",
        "take_photo",
        "camera_status",
        "live_preview",
        "stop_preview",

        # Communication
        "open_whatsapp",
        "send_whatsapp",
        "open_email",
        "compose_email",

        # Memory
        "remember",
        "recall_memory",
        "forget_memory",
        "show_memory",

        # Plugins
        "list_plugins",
        "enable_plugin",
        "disable_plugin",
        "reload_plugins",
        "reload_plugin",
        "create_plugin",
        "uninstall_plugin",
        "execute_plugin",

        # Conversation
        "unknown",
    }

    # ============================================================
    # INTENT ALIASES
    # ============================================================

    INTENT_ALIASES = {

        # -------------------------
        # System
        # -------------------------

        "computer_status": "system_status",
        "system_info": "system_status",
        "system_information": "system_status",
        "pc_status": "system_status",
        "computer_information": "system_status",

        "cpu": "cpu_usage",
        "processor_usage": "cpu_usage",

        "ram": "ram_usage",
        "memory_usage": "ram_usage",
        "memory_status": "ram_usage",

        "disk": "disk_space",
        "disk_usage": "disk_space",
        "storage": "disk_space",
        "storage_usage": "disk_space",

        "internet": "internet_status",
        "connection_status": "internet_status",
        "internet_connection": "internet_status",

        "speed_test": "internet_speed",
        "network_speed": "internet_speed",
        "internet_speed_test": "internet_speed",

        # -------------------------
        # Time
        # -------------------------

        "time": "get_time",
        "current_time": "get_time",
        "date": "get_date",
        "current_date": "get_date",

        # -------------------------
        # Volume
        # -------------------------

        "volume_status": "get_volume",
        "volume_level": "get_volume",
        "sound_level": "get_volume",

        "volume_up": "increase_volume",
        "increase_sound": "increase_volume",
        "sound_up": "increase_volume",

        "volume_down": "decrease_volume",
        "decrease_sound": "decrease_volume",
        "sound_down": "decrease_volume",

        "mute": "mute_volume",
        "mute_sound": "mute_volume",

        "unmute": "unmute_volume",
        "unmute_sound": "unmute_volume",

        # -------------------------
        # Screenshot
        # -------------------------

        "take_screenshot": "screenshot",
        "screen_capture": "screenshot",
        "capture_screen": "screenshot",
        "capture_screenshot": "screenshot",

        # -------------------------
        # Clipboard
        # -------------------------

        "get_clipboard": "read_clipboard",
        "show_clipboard": "read_clipboard",
        "read_clipboard_content": "read_clipboard",

        "copy": "copy_to_clipboard",

        "empty_clipboard": "clear_clipboard",

        # -------------------------
        # Applications
        # -------------------------

        "open_app": "open_application",
        "launch_app": "open_application",
        "start_app": "open_application",
        "launch_application": "open_application",
        "start_application": "open_application",

        "close_app": "close_application",
        "exit_app": "close_application",
        "quit_application": "close_application",

        "minimize_app": "minimize_application",
        "hide_application": "minimize_application",

        "maximize_app": "maximize_application",
        "full_screen_application": "maximize_application",

        "switch_app": "switch_application",
        "focus_application": "switch_application",

        # -------------------------
        # Windows
        # -------------------------

        "active_window": "get_active_window",
        "current_window": "get_active_window",

        "list_windows": "get_open_windows",
        "show_windows": "get_open_windows",
        "open_windows": "get_open_windows",

        "minimize_all": "minimize_all_windows",
        "minimize_everything": "minimize_all_windows",

        "restore_all": "restore_all_windows",
        "restore_windows": "restore_all_windows",

        "next_app": "next_window",
        "previous_app": "previous_window",

        "move_window": "move_application",
        "move_app": "move_application",

        # -------------------------
        # Browser
        # -------------------------

        "search_google": "google_search",
        "search_on_google": "google_search",

        "search_youtube": "youtube_search",
        "search_on_youtube": "youtube_search",

        "open_url": "open_website",
        "open_site": "open_website",
        "visit_website": "open_website",

        "check_weather": "weather",
        "weather_check": "weather",

        "search_news": "news_search",
        "latest_news": "news_search",

        # -------------------------
        # Files
        # -------------------------

        "find_file": "search_file",
        "locate_file": "search_file",

        "get_file_info": "file_info",
        "file_details": "file_info",

        "rename": "rename_file",
        "rename_file_name": "rename_file",

        "move": "move_file",
        "move_file_to": "move_file",

        "remove_file": "delete_file",
        "delete": "delete_file",

        "source_location": "source_location",
        "source_folder": "source_location",
        "from_folder": "source_location",
        "source_directory": "source_location",

        # -------------------------
        # Folders
        # -------------------------

        "desktop": "open_desktop",
        "downloads": "open_downloads",
        "documents": "open_documents",
        "pictures": "open_pictures",
        "music": "open_music",
        "videos": "open_videos",

        # -------------------------
        # Reminders
        # -------------------------

        "set_reminder": "create_reminder",
        "add_reminder": "create_reminder",

        "show_reminders": "list_reminders",
        "get_reminders": "list_reminders",

        "remove_reminder": "cancel_reminder",
        "delete_reminder": "cancel_reminder",

        # -------------------------
        # Camera
        # -------------------------

        "camera": "open_camera",
        "start_camera": "open_camera",

        "stop_camera": "close_camera",

        "photo": "take_photo",
        "capture_photo": "take_photo",

        "camera_preview": "live_preview",
        "start_preview": "live_preview",

        # -------------------------
        # Communication
        # -------------------------

        "whatsapp": "open_whatsapp",
        "send_whatsapp_message": "send_whatsapp",

        "email": "open_email",
        "send_email": "compose_email",

        # -------------------------
        # Memory
        # -------------------------

        "save_memory": "remember",
        "remember_this": "remember",

        "recall": "recall_memory",
        "get_memory": "recall_memory",

        "delete_memory": "forget_memory",
        "remove_memory": "forget_memory",

        "show_saved_memory": "show_memory",

        # -------------------------
        # Plugins
        # -------------------------

        "plugins": "list_plugins",
        "show_plugins": "list_plugins",

        "activate_plugin": "enable_plugin",
        "turn_on_plugin": "enable_plugin",

        "deactivate_plugin": "disable_plugin",
        "turn_off_plugin": "disable_plugin",

        "refresh_plugins": "reload_plugins",
        "refresh_all_plugins": "reload_plugins",

        "refresh_plugin": "reload_plugin",

        "remove_plugin": "uninstall_plugin",
        "delete_plugin": "uninstall_plugin",

        "run_plugin": "execute_plugin",
    }

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self):

        # =========================
        # Memory
        # =========================

        self.memory = MemoryManager()

        # =========================
        # Gemini
        # =========================

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )
        self.model_name = MODEL_NAME
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        # =========================
        # Offline AI / Ollama
        # =========================

        self.offline_model = "llama3.2:3b"

        self.offline_url = (
            "http://localhost:11434/api/generate"
        )

        # =========================
        # Conversation
        # =========================

        self.conversation_context = []

        self.offline_history = []

        self.max_history = 10
        self.max_context = 10

    # ============================================================
    # NORMALIZE AI INTENT
    # ============================================================

    def normalize_intent(self, intent):

        if not intent:
            return "unknown"

        intent = str(
            intent
        ).strip().lower()

        intent = self.INTENT_ALIASES.get(
            intent,
            intent
        )

        if intent not in self.VALID_INTENTS:

            return "unknown"

        return intent

    # ============================================================
    # EXTRACT JSON
    # ============================================================

    def extract_json(self, text):

        if not text:

            raise ValueError(
                "Empty AI response"
            )

        text = text.strip()

        # Remove markdown code fences
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

        text = text.strip()

        # Direct JSON
        try:

            return json.loads(
                text
            )

        except json.JSONDecodeError:

            pass

        # Find JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:

            raise ValueError(
                "No JSON object found"
            )

        json_text = text[
            start:end + 1
        ]

        return json.loads(
            json_text
        )

    # ============================================================
    # NORMALIZE PARAMETERS
    # ============================================================

    def normalize_parameters(
        self,
        intent,
        parameters
    ):

        if not isinstance(
            parameters,
            dict
        ):

            parameters = {}

        # -------------------------
        # Plugin parameter aliases
        # -------------------------

        if intent in [
            "enable_plugin",
            "disable_plugin",
            "reload_plugin",
            "create_plugin",
            "uninstall_plugin",
            "execute_plugin",
        ]:

            if not parameters.get("name"):

                for key in [
                    "plugin",
                    "plugin_name"
                ]:

                    if parameters.get(key):

                        parameters["name"] = (
                            parameters[key]
                        )

                        break

        # -------------------------
        # Application parameter
        # -------------------------

        if intent in [
            "open_application",
            "close_application",
            "minimize_application",
            "maximize_application",
            "switch_application",
            "move_application",
        ]:

            if not parameters.get("app"):

                for key in [
                    "application",
                    "application_name",
                    "program"
                ]:

                    if parameters.get(key):

                        parameters["app"] = (
                            parameters[key]
                        )

                        break

        # -------------------------
        # Search parameter
        # -------------------------

        if intent in [
            "google_search",
            "youtube_search",
            "news_search",
        ]:

            if not parameters.get("query"):

                for key in [
                    "search",
                    "search_query",
                    "text"
                ]:

                    if parameters.get(key):

                        parameters["query"] = (
                            parameters[key]
                        )

                        break

        # -------------------------
        # Website
        # -------------------------

        if intent == "open_website":

            url = parameters.get(
                "url"
            )

            if url and not re.match(
                r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
                str(url)
            ):

                parameters["url"] = (
                    "https://" + str(url)
                )

        # -------------------------
        # Volume
        # -------------------------

        if intent == "set_volume":

            level = parameters.get(
                "level"
            )

            try:

                level = int(level)

                parameters["level"] = max(
                    0,
                    min(100, level)
                )

            except (
                TypeError,
                ValueError
            ):

                parameters["level"] = None

        # -------------------------
        # Move application
        # -------------------------

        if intent == "move_application":

            for key in [
                "x",
                "y"
            ]:

                if key in parameters:

                    try:

                        parameters[key] = int(
                            parameters[key]
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        parameters[key] = None

        # -------------------------
        # Reminder
        # -------------------------

        if intent == "create_reminder":

            if not parameters.get("text"):

                if parameters.get(
                    "message"
                ):

                    parameters["text"] = (
                        parameters["message"]
                    )

            if not parameters.get("time"):

                if parameters.get(
                    "datetime"
                ):

                    parameters["time"] = (
                        parameters["datetime"]
                    )

        # -------------------------
        # WhatsApp
        # -------------------------

        if intent == "send_whatsapp":

            if not parameters.get(
                "recipient"
            ):

                for key in [
                    "name",
                    "contact",
                    "person"
                ]:

                    if parameters.get(key):

                        parameters["recipient"] = (
                            parameters[key]
                        )

                        break

            if not parameters.get(
                "message"
            ):

                for key in [
                    "text",
                    "body"
                ]:

                    if parameters.get(key):

                        parameters["message"] = (
                            parameters[key]
                        )

                        break

        # -------------------------
        # Email
        # -------------------------

        if intent == "compose_email":

            if not parameters.get(
                "recipient"
            ):

                if parameters.get(
                    "email"
                ):

                    parameters["recipient"] = (
                        parameters["email"]
                    )

        # -------------------------
        # Dynamic File Management
        # -------------------------

        if intent == "files":

            if not parameters.get("name"):

                for key in [
                    "folder_name",
                    "file_name",
                    "filename",
                    "folder"
                ]:

                    if parameters.get(key):

                        parameters["name"] = (
                            parameters[key]
                        )

                        break

            if not parameters.get("location"):

                for key in [
                    "path",
                    "directory",
                    "destination",
                    "parent_folder",
                    "inside"
                ]:

                    if parameters.get(key):

                        parameters["location"] = (
                            parameters[key]
                        )

                        break

            if not parameters.get("content"):

                for key in [
                    "text",
                    "body"
                ]:

                    if parameters.get(key):

                        parameters["content"] = (
                            parameters[key]
                        )

                        break

            if not parameters.get("source"):

                if parameters.get("from"):

                    parameters["source"] = (
                        parameters["from"]
                    )

            if not parameters.get("destination"):

                for key in [
                    "target",
                    "destination_folder",
                    "to"
                ]:

                    if parameters.get(key):

                        parameters["destination"] = (
                            parameters[key]
                        )

                        break

            if not parameters.get("old_name"):

                if parameters.get("old"):

                    parameters["old_name"] = (
                        parameters["old"]
                    )

            if not parameters.get("new_name"):

                if parameters.get("new"):

                    parameters["new_name"] = (
                        parameters["new"]
                    )
        # -------------------------
        # File parameters
        # -------------------------

        if intent in [
            "read_file",
            "file_info",
            "delete_file",
        ]:

            if not parameters.get(
                "path"
            ):

                for key in [
                    "file",
                    "file_path",
                    "name"
                ]:

                    if parameters.get(key):

                        parameters["path"] = (
                            parameters[key]
                        )

                        break

        if intent == "search_file":

            if not parameters.get(
                "query"
            ):

                for key in [
                    "file",
                    "filename",
                    "name"
                ]:

                    if parameters.get(key):

                        parameters["query"] = (
                            parameters[key]
                        )

                        break

        if intent == "rename_file":

            if not parameters.get(
                "old_name"
            ):

                if parameters.get(
                    "old"
                ):

                    parameters["old_name"] = (
                        parameters["old"]
                    )

            if not parameters.get(
                "new_name"
            ):

                if parameters.get(
                    "new"
                ):

                    parameters["new_name"] = (
                        parameters["new"]
                    )

        if intent == "move_file":

            if not parameters.get(
                "source"
            ):

                if parameters.get(
                    "path"
                ):

                    parameters["source"] = (
                        parameters["path"]
                    )

            if not parameters.get(
                "destination"
            ):

                for key in [
                    "destination_folder",
                    "folder",
                    "target"
                ]:

                    if parameters.get(key):

                        parameters["destination"] = (
                            parameters[key]
                        )

                        break

        # -------------------------
        # Memory
        # -------------------------

        if intent == "remember":

            if not parameters.get(
                "value"
            ):

                if parameters.get(
                    "text"
                ):

                    parameters["value"] = (
                        parameters["text"]
                    )

        return parameters

    # ============================================================
    # AI INTENT CLASSIFIER
    # ============================================================

    def classify_intent(
        self,
        user_text
    ):

        """
        Understand a natural-language JARVIS command.

        This function ONLY understands the command.

        It does NOT execute anything.

        Returns:

        {
            "intent": "...",
            "parameters": {}
        }
        """

        if not user_text:

            return {
                "intent": "unknown",
                "parameters": {}
            }

        prompt = f"""
        You are the command understanding engine of JARVIS,
        a Windows desktop AI assistant.

        Your job is ONLY to understand the user's command.

        DO NOT answer the user.

        DO NOT execute anything.

        DO NOT explain anything.

        Return ONLY valid JSON.

        Required format:

        {{
            "intent": "intent_name",
            "parameters": {{}}
        }}


        ============================================================
        AVAILABLE INTENTS
        ============================================================

        SYSTEM:
        system_status
        battery
        cpu_usage
        ram_usage
        disk_space
        internet_status
        internet_speed

        TIME:
        get_time
        get_date

        VOLUME:
        get_volume
        increase_volume
        decrease_volume
        mute_volume
        unmute_volume
        set_volume

        POWER:
        lock_pc
        shutdown_pc
        restart_pc

        SCREEN:
        screenshot

        CLIPBOARD:
        read_clipboard
        copy_to_clipboard
        clear_clipboard

        APPLICATIONS:
        open_application
        close_application
        minimize_application
        maximize_application
        switch_application
        get_active_window
        get_open_windows
        minimize_all_windows
        restore_all_windows
        next_window
        previous_window
        move_application

        BROWSER:
        open_google
        open_youtube
        open_github
        google_search
        youtube_search
        open_website
        weather
        news_search

        FILES:
        files

        When intent is "files", ALWAYS provide an "action".

        Allowed file actions:

        create_folder
        create_file
        write_file
        append_file
        read_file
        search_file
        file_info
        rename_file
        move_file
        delete_file

        For file operations, return:

        {{
            "intent": "files",
            "action": "action_name",
            "parameters": {{}}
        }}

        FOLDERS:
        open_desktop
        open_downloads
        open_documents
        open_pictures
        open_music
        open_videos

        REMINDERS:
        create_reminder
        list_reminders
        cancel_reminder

        CAMERA:
        open_camera
        close_camera
        take_photo
        camera_status
        live_preview
        stop_preview

        COMMUNICATION:
        open_whatsapp
        send_whatsapp
        open_email
        compose_email

        MEMORY:
        remember
        recall_memory
        forget_memory
        show_memory

        PLUGINS:
        list_plugins
        enable_plugin
        disable_plugin
        reload_plugins
        reload_plugin
        create_plugin
        uninstall_plugin
        execute_plugin

        OTHER:
        unknown


        ============================================================
        IMPORTANT UNDERSTANDING RULES
        ============================================================

        1. Understand natural language.

        2. Do NOT require exact command phrases.

        3. Understand synonyms.

        4. Understand polite requests.

        5. Understand simple Banglish where possible.

        6. Extract parameters.

        7. Preserve file paths.

        8. Preserve search queries.

        9. Do not invent missing information.

        10. If required information is missing, keep that parameter empty.

        11. Conversation such as:
        "hello"
        "hi"
        "how are you"
        "tell me a joke"
        "what are you doing"

        must return:

        {{
            "intent": "unknown",
            "parameters": {{}}
        }}

        12. If unsure, return unknown.

        13. Return ONLY JSON.

        ============================================================
        EXAMPLES
        ============================================================

        User:
        "what is my computer status"

        Output:
        {{
            "intent": "system_status",
            "parameters": {{}}
        }}

        User:
        "how much RAM am I using"

        Output:
        {{
            "intent": "ram_usage",
            "parameters": {{}}
        }}

        User:
        "amar CPU usage koto"

        Output:
        {{
            "intent": "cpu_usage",
            "parameters": {{}}
        }}

        User:
        "volume ta komao"

        Output:
        {{
            "intent": "decrease_volume",
            "parameters": {{}}
        }}

        User:
        "set volume to 40"

        Output:
        {{
            "intent": "set_volume",
            "parameters": {{
                "level": 40
            }}
        }}

        User:
        "open chrome"

        Output:
        {{
            "intent": "open_application",
            "parameters": {{
                "app": "chrome"
            }}
        }}

        User:
        "chrome ta open koro"

        Output:
        {{
            "intent": "open_application",
            "parameters": {{
                "app": "chrome"
            }}
        }}

        User:
        "close calculator"

        Output:
        {{
            "intent": "close_application",
            "parameters": {{
                "app": "calculator"
            }}
        }}

        User:
        "switch to vscode"

        Output:
        {{
            "intent": "switch_application",
            "parameters": {{
                "app": "vscode"
            }}
        }}

        User:
        "what window is active"

        Output:
        {{
            "intent": "get_active_window",
            "parameters": {{}}
        }}

        User:
        "show me all open windows"

        Output:
        {{
            "intent": "get_open_windows",
            "parameters": {{}}
        }}

        User:
        "minimize everything"

        Output:
        {{
            "intent": "minimize_all_windows",
            "parameters": {{}}
        }}

        User:
        "restore all windows"

        Output:
        {{
            "intent": "restore_all_windows",
            "parameters": {{}}
        }}

        User:
        "move chrome to 100,200"

        Output:
        {{
            "intent": "move_application",
            "parameters": {{
                "app": "chrome",
                "x": 100,
                "y": 200
            }}
        }}

        User:
        "search Google for Laravel 8 tutorial"

        Output:
        {{
            "intent": "google_search",
            "parameters": {{
                "query": "Laravel 8 tutorial"
            }}
        }}

        User:
        "search YouTube for Python tutorial"

        Output:
        {{
            "intent": "youtube_search",
            "parameters": {{
                "query": "Python tutorial"
            }}
        }}

        User:
        "open facebook.com"

        Output:
        {{
            "intent": "open_website",
            "parameters": {{
                "url": "https://facebook.com"
            }}
        }}

        User:
        "weather in Dhaka"

        Output:
        {{
            "intent": "weather",
            "parameters": {{
                "location": "Dhaka"
            }}
        }}

        User:
        "latest news about AI"

        Output:
        {{
            "intent": "news_search",
            "parameters": {{
                "query": "AI"
            }}
        }}

        User:
        "create a folder called projects"

        Output:
        {{
            "intent": "files",
            "action": "create_folder",
            "parameters": {{
                "name": "Laravel",
                "location": "project folder"
            }}
        }}

        User:
        "create test.txt"

        Output:
        {{
            "intent": "create_file",
            "parameters": {{
                "name": "test.txt"
            }}
        }}

        User:
        "write hello world to test.txt"

        Output:
        {{
            "intent": "write_file",
            "parameters": {{
                "path": "test.txt",
                "content": "hello world"
            }}
        }}

        User:
        "read test.txt"

        Output:
        {{
            "intent": "read_file",
            "parameters": {{
                "path": "test.txt"
            }}
        }}

        User:
        "find test.txt"

        Output:
        {{
            "intent": "search_file",
            "parameters": {{
                "query": "test.txt"
            }}
        }}

        User:
        "rename test.txt to hello.txt"

        Output:
        {{
            "intent": "rename_file",
            "parameters": {{
                "old_name": "test.txt",
                "new_name": "hello.txt"
            }}
        }}

        User:
        "move test.txt to Documents"

        Output:
        {{
            "intent": "files",
            "action": "move_file",
            "parameters": {{
                "source": "test.txt",
                "source_location": "my project folder",
                "destination": "my Laravel project"
            }}
        }}

        User:
        "delete test.txt"

        Output:
        {{
            "intent": "delete_file",
            "parameters": {{
                "path": "test.txt"
            }}
        }}

        User:
        "open my downloads folder"

        Output:
        {{
            "intent": "open_downloads",
            "parameters": {{}}
        }}

        User:
        "remind me at 5 pm to call Rahim"

        Output:
        {{
            "intent": "create_reminder",
            "parameters": {{
                "text": "call Rahim",
                "time": "5 pm"
            }}
        }}

        User:
        "show my reminders"

        Output:
        {{
            "intent": "list_reminders",
            "parameters": {{}}
        }}

        User:
        "open camera"

        Output:
        {{
            "intent": "open_camera",
            "parameters": {{}}
        }}

        User:
        "take a photo"

        Output:
        {{
            "intent": "take_photo",
            "parameters": {{}}
        }}

        User:
        "send WhatsApp to Rahim saying I am coming"

        Output:
        {{
            "intent": "send_whatsapp",
            "parameters": {{
                "recipient": "Rahim",
                "message": "I am coming"
            }}
        }}

        User:
        "remember my name is Tarek"

        Output:
        {{
            "intent": "remember",
            "parameters": {{
                "key": "name",
                "value": "Tarek"
            }}
        }}

        User:
        "what is my name"

        Output:
        {{
            "intent": "recall_memory",
            "parameters": {{
                "key": "name"
            }}
        }}

        User:
        "show my plugins"

        Output:
        {{
            "intent": "list_plugins",
            "parameters": {{}}
        }}

        User:
        "enable weather plugin"

        Output:
        {{
            "intent": "enable_plugin",
            "parameters": {{
                "name": "weather"
            }}
        }}

        User:
        "disable weather plugin"

        Output:
        {{
            "intent": "disable_plugin",
            "parameters": {{
                "name": "weather"
            }}
        }}

        User:
        "reload plugins"

        Output:
        {{
            "intent": "reload_plugins",
            "parameters": {{}}
        }}


        ============================================================
        CURRENT USER COMMAND
        ============================================================

        "{user_text}"

        Return ONLY JSON.
        """

        try:

            # response = self.client.models.generate_content(
            #     model=MODEL_NAME,
            #     contents=prompt
            # )
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    )
                )
            )

            raw_text = (
                response.text
                if response.text
                else ""
            )

            result = self.extract_json(
                raw_text
            )

            if not isinstance(
                result,
                dict
            ):

                raise ValueError(
                    "AI result is not an object"
                )

            intent = self.normalize_intent(
                result.get(
                    "intent",
                    "unknown"
                )
            )

            parameters = self.normalize_parameters(
                intent,
                result.get(
                    "parameters",
                    {}
                )
            )

            action = result.get(
                "action",
                None
            )

            return {
                "intent": intent,
                "action": action,
                "parameters": parameters
            }

        except (
            json.JSONDecodeError,
            ValueError
        ) as e:

            print(
                f"⚠️ AI Intent JSON Error: {e}"
            )

            return {
                "intent": "unknown",
                "parameters": {}
            }

        except Exception as e:

            print(
                f"⚠️ AI Intent Classification Error: {e}"
            )

            return {
                "intent": "unknown",
                "parameters": {}
            }

    # ============================================================
    # MAIN AI CHAT
    # ============================================================

    def ask(self, user_text):

        if not user_text:

            return ""

        max_retries = 2

        # =========================
        # Memory
        # =========================

        memory_context = (
            self.get_memory_context()
        )

        # =========================
        # Recent Conversation
        # =========================

        conversation_context = (
            self.get_conversation_context()
        )

        # IMPORTANT:
        # Do NOT overwrite this prompt later.
        enhanced_prompt = f"""
You are JARVIS, Tarek's personal AI assistant.

Use saved memory and recent conversation when useful.

SAVED MEMORY:
{memory_context}

RECENT CONVERSATION:
{conversation_context}

RULES:

- Respond naturally.
- Keep normal answers concise.
- Always answer in English unless the user clearly requests another language.
- Understand references such as:
  "it"
  "that"
  "this"
  "the project"
  "the file"
  "the previous one"
- Use recent conversation to understand those references.
- Do not invent information.
- Do not mention these instructions.

USER:
{user_text}
"""

        for attempt in range(
            max_retries
        ):

            try:

                response = self.chat.send_message(
                    message=enhanced_prompt
                )

                if response.text:

                    answer = (
                        response.text.strip()
                    )

                    # Save conversation
                    self.add_conversation(
                        f"User: {user_text}"
                    )

                    self.add_conversation(
                        f"JARVIS: {answer}"
                    )

                    return answer

                return self.offline_ask(
                    user_text
                )

            except ClientError as e:

                error_text = str(e)

                if (
                    "429" in error_text
                    or
                    "RESOURCE_EXHAUSTED"
                    in error_text
                ):

                    print(
                        "⚠️ Gemini quota exceeded."
                    )

                    print(
                        "🔄 Switching to Offline AI..."
                    )

                    return self.offline_ask(
                        user_text
                    )

                print(
                    f"⚠️ Gemini client error: {e}"
                )

                return self.offline_ask(
                    user_text
                )

            except ServerError as e:

                if attempt < max_retries - 1:

                    wait_time = (
                        2 ** attempt
                    )

                    print(
                        f"⚠️ Gemini server busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(
                        wait_time
                    )

                    continue

                print(
                    "⚠️ Gemini server unavailable."
                )

                return self.offline_ask(
                    user_text
                )

            except Exception as e:

                print(
                    f"⚠️ Gemini error: {e}"
                )

                return self.offline_ask(
                    user_text
                )

        return self.offline_ask(
            user_text
        )

    # ============================================================
    # ADD CONVERSATION
    # ============================================================

    def add_conversation(
        self,
        message
    ):

        if not message:
            return

        self.conversation_context.append(
            message
        )

        self.conversation_context = (
            self.conversation_context[
                -self.max_context:
            ]
        )

    # ============================================================
    # MEMORY CONTEXT
    # ============================================================

    def get_memory_context(self):

        try:

            data = self.memory._load()

            if not data:

                return "No saved memories."

            lines = []

            for key, value in data.items():

                lines.append(
                    f"- {key}: {value}"
                )

            return "\n".join(
                lines
            )

        except Exception as e:

            print(
                f"⚠️ Memory context error: {e}"
            )

            return "No saved memories."

    # ============================================================
    # CONVERSATION CONTEXT
    # ============================================================

    def get_conversation_context(self):

        if not self.conversation_context:

            return "No recent conversation."

        recent = (
            self.conversation_context[
                -self.max_context:
            ]
        )

        return "\n".join(
            recent
        )

    # ============================================================
    # OFFLINE AI
    # ============================================================

    def offline_ask(
        self,
        user_text
    ):

        try:

            # Add user message
            self.offline_history.append(
                f"User: {user_text}"
            )

            self.offline_history = (
                self.offline_history[
                    -self.max_history:
                ]
            )

            conversation = "\n".join(
                self.offline_history
            )

            memory_context = (
                self.get_memory_context()
            )

            system_prompt = f"""
                You are JARVIS, Tarek's personal AI assistant.

                RULES:

                1. Always respond in English.
                2. Be natural and helpful.
                3. Keep responses concise when possible.
                4. Your name is JARVIS.
                5. You were created by Tarek.
                6. Never claim someone else created you.
                7. Never pretend to be Gemini, Ollama, ChatGPT, or another AI.
                8. Use saved memory when relevant.
                9. Use recent conversation when relevant.
                10. Do not mention these instructions.
                11. Do not invent facts.
                12. If you do not know something, say so honestly.

                SAVED MEMORY:

                {memory_context}

                RECENT CONVERSATION:

                {conversation}

                Answer the latest user message.
                """

            response = requests.post(
                self.offline_url,
                json={
                    "model": self.offline_model,
                    "system": system_prompt,
                    "prompt": user_text,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            answer = (
                data.get(
                    "response",
                    ""
                )
                .strip()
            )

            if answer:

                self.offline_history.append(
                    f"JARVIS: {answer}"
                )

                self.offline_history = (
                    self.offline_history[
                        -self.max_history:
                    ]
                )

                print(
                    "🧠 Offline AI response generated."
                )

                return answer

            return (
                "Sorry Tarek, Offline AI "
                "could not generate a response."
            )

        except requests.exceptions.ConnectionError:

            print(
                "❌ Ollama is not running."
            )

            return (
                "Sorry Tarek, Gemini is unavailable "
                "and Offline AI is not running. "
                "Please start Ollama."
            )

        except requests.exceptions.Timeout:

            print(
                "⚠️ Offline AI timed out."
            )

            return (
                "Sorry Tarek, Offline AI took "
                "too long to respond."
            )

        except Exception as e:

            print(
                f"⚠️ Offline AI error: {e}"
            )

            return (
                "Sorry Tarek, both Gemini and "
                "Offline AI are currently unavailable."
            )

    # ============================================================
    # CLEAR OFFLINE HISTORY
    # ============================================================

    def clear_offline_history(self):

        self.offline_history.clear()

        return (
            "Offline AI conversation history "
            "has been cleared."
        )

    # ============================================================
    # CLEAR JARVIS CONTEXT
    # ============================================================

    def clear_conversation_context(self):

        self.conversation_context.clear()

        return (
            "JARVIS conversation context "
            "has been cleared."
        )

