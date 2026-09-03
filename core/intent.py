import re
from core.memory import MemoryManager
from core.confirmation import ConfirmationManager

from tools.system_tools import (
    get_time,
    get_date,
    lock_pc,
    shutdown_pc,
    restart_pc,
    get_battery_status,
    get_cpu_usage,
    get_ram_usage,
    get_disk_space,
    get_internet_status,
    get_volume,
    set_volume,
    increase_volume,
    decrease_volume,
    mute_volume,
    unmute_volume,
)

from tools.browser_tools import (
    open_youtube,
    open_google,
    open_github,
    search_google,
    search_youtube,
    open_website,
    get_weather,
    news_search,
)

from tools.app_tools import (
    open_notepad,
    open_calculator,
    open_explorer,
    open_command_prompt,
    open_powershell,
    open_vscode,
    open_chrome,
    close_app,
    minimize_all_windows,
    show_desktop,
)

from tools.file_tools import (
    open_desktop,
    open_downloads,
    open_documents,
    open_pictures,
    open_music,
    open_videos,
    create_folder,
    create_text_file,
    rename_item,
    move_item,
    search_files,
    open_path,
    get_file_info,
    get_recent_files,
    delete_item,
    empty_recycle_bin,
)


class IntentManager:

    def __init__(self):
        self.memory = MemoryManager()
        self.confirmation = ConfirmationManager()

        self.commands = {

            # =========================
            # System
            # =========================

            "time": {
                "keywords": [
                    "time",
                    "what time",
                    "current time",
                    "kota baje",
                    "koita baje",
                    "কয়টা বাজে",
                    "কটা বাজে",
                ],
                "function": get_time,
            },

            "date": {
                "keywords": [
                    "date",
                    "today date",
                    "current date",
                    "ajker date",
                    "ajke koto tarikh",
                    "আজকের তারিখ",
                    "আজ কত তারিখ",
                ],
                "function": get_date,
            },

            "lock": {
                "keywords": [
                    "lock pc",
                    "lock computer",
                    "lock my pc",
                    "pc lock koro",
                    "কম্পিউটার লক",
                    "পিসি লক",
                ],
                "function": lock_pc,
            },

            # =========================
            # Browser
            # =========================

            "youtube": {
                "keywords": [
                    "open youtube",
                    "youtube kholo",
                    "youtube open",
                    "open youtube please",
                    "ইউটিউব খুলো",
                    "ইউটিউব খুলে দাও",
                ],
                "function": open_youtube,
            },

            "google": {
                "keywords": [
                    "open google",
                    "google kholo",
                    "google open",
                    "open google please",
                    "গুগল খুলো",
                    "গুগল খুলে দাও",
                ],
                "function": open_google,
            },

            "github": {
                "keywords": [
                    "open github",
                    "github kholo",
                    "github open",
                    "গিটহাব খুলো",
                    "গিটহাব খুলে দাও",
                ],
                "function": open_github,
            },

            # =========================
            # Applications
            # =========================

            "notepad": {
                "keywords": [
                    "open notepad",
                    "notepad kholo",
                    "notepad open",
                    "open notepad please",
                    "নোটপ্যাড খুলো",
                    "নোটপ্যাড খুলে দাও",
                ],
                "function": open_notepad,
            },

            "calculator": {
                "keywords": [
                    "open calculator",
                    "calculator kholo",
                    "calculator open",
                    "open calculator please",
                    "ক্যালকুলেটর খুলো",
                    "ক্যালকুলেটর খুলে দাও",
                ],
                "function": open_calculator,
            },

            "explorer": {
                "keywords": [
                    "open file explorer",
                    "open explorer",
                    "file explorer kholo",
                    "explorer kholo",
                    "ফাইল এক্সপ্লোরার খুলো",
                ],
                "function": open_explorer,
            },

            "cmd": {
                "keywords": [
                    "open command prompt",
                    "open cmd",
                    "cmd kholo",
                    "command prompt kholo",
                    "কমান্ড প্রম্পট খুলো",
                ],
                "function": open_command_prompt,
            },

            "powershell": {
                "keywords": [
                    "open powershell",
                    "powershell kholo",
                    "powershell open",
                    "পাওয়ারশেল খুলো",
                ],
                "function": open_powershell,
            },

            "vscode": {
                "keywords": [
                    "open vscode",
                    "open vs code",
                    "vscode kholo",
                    "vs code kholo",
                    "visual studio code kholo",
                    "ভিএস কোড খুলো",
                ],
                "function": open_vscode,
            },

            "chrome": {
                "keywords": [
                    "open chrome",
                    "chrome kholo",
                    "chrome open",
                    "open chrome please",
                    "ক্রোম খুলো",
                    "ক্রোম খুলে দাও",
                ],
                "function": open_chrome,
            },

            # =========================
            # Folders
            # =========================

            "desktop": {
                "keywords": [
                    "open desktop",
                    "desktop kholo",
                    "desktop open",
                    "ডেস্কটপ খুলো",
                    "ডেস্কটপ খুলে দাও",
                ],
                "function": open_desktop,
            },

            "downloads": {
                "keywords": [
                    "open downloads",
                    "downloads kholo",
                    "downloads open",
                    "ডাউনলোড খুলো",
                    "ডাউনলোডস খুলো",
                ],
                "function": open_downloads,
            },

            "documents": {
                "keywords": [
                    "open documents",
                    "documents kholo",
                    "documents open",
                    "ডকুমেন্টস খুলো",
                ],
                "function": open_documents,
            },

            "pictures": {
                "keywords": [
                    "open pictures",
                    "pictures kholo",
                    "pictures open",
                    "ছবির ফোল্ডার খুলো",
                ],
                "function": open_pictures,
            },

            "music": {
                "keywords": [
                    "open music",
                    "music kholo",
                    "music open",
                    "মিউজিক খুলো",
                ],
                "function": open_music,
            },

            "videos": {
                "keywords": [
                    "open videos",
                    "videos kholo",
                    "videos open",
                    "ভিডিও ফোল্ডার খুলো",
                ],
                "function": open_videos,
            },
            "battery": {
                "keywords": [
                    "battery",
                    "battery percentage",
                    "battery status",
                    "how much battery",
                    "চার্জ কত",
                    "ব্যাটারি কত",
                ],
                "function": get_battery_status,
            },

            "cpu": {
                "keywords": [
                    "cpu usage",
                    "cpu status",
                    "processor usage",
                    "সিপিইউ কত",
                ],
                "function": get_cpu_usage,
            },

            "ram": {
                "keywords": [
                    "ram usage",
                    "memory usage",
                    "ram status",
                    "র‍্যাম কত",
                    "মেমোরি কত",
                ],
                "function": get_ram_usage,
            },

            "disk": {
                "keywords": [
                    "disk space",
                    "disk usage",
                    "c drive space",
                    "hard disk space",
                    "ডিস্ক স্পেস",
                ],
                "function": get_disk_space,
            },

            "internet": {
                "keywords": [
                    "internet status",
                    "internet connection",
                    "is internet working",
                    "ইন্টারনেট চলছে",
                    "ইন্টারনেট কানেকশন",
                ],
                "function": get_internet_status,
            },
            
        }

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

            text = text.replace(word, " ")

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # =========================
    # Dynamic Google Search
    # =========================

    def google_search_intent(self, command):

        patterns = [
            r"search google for (.+)",
            r"search google (.+)",
            r"google search (.+)",
            r"search (.+) on google",
            r"google e (.+)",
            r"google te (.+)",
            r"গুগলে (.+) সার্চ",
            r"গুগলে (.+) খুঁজে",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                query = match.group(1).strip()

                # Remove trailing natural-language words
                query = re.sub(
                    r"\s+(search|khojo|khuj|করো|দাও)$",
                    "",
                    query,
                    flags=re.IGNORECASE
                )

                return search_google(query)

        return None

    # =========================
    # Dynamic YouTube Search
    # =========================

    def youtube_search_intent(self, command):

        patterns = [
            r"search youtube for (.+)",
            r"search youtube (.+)",
            r"youtube search (.+)",
            r"search (.+) on youtube",
            r"youtube e (.+)",
            r"youtube te (.+)",
            r"ইউটিউবে (.+) সার্চ",
            r"ইউটিউবে (.+) খুঁজে",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                query = match.group(1).strip()

                query = re.sub(
                    r"\s+(search|khojo|khuj|করো|দাও)$",
                    "",
                    query,
                    flags=re.IGNORECASE
                )

                return search_youtube(query)

        return None

    # =========================
    # Create Folder
    # =========================

    def create_folder_intent(self, command):

        patterns = [
            r"create folder (.+)",
            r"make folder (.+)",
            r"new folder (.+)",
            r"create a folder (.+)",
            r"make a folder (.+)",
            r"folder (.+) create koro",
            r"ফোল্ডার (.+) তৈরি করো",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                return create_folder(
                    match.group(1).strip()
                )

        return None

    # =========================
    # Create Text File
    # =========================

    def create_file_intent(self, command):

        patterns = [
            r"create text file (.+)",
            r"create file (.+)",
            r"make text file (.+)",
            r"make file (.+)",
            r"create a text file (.+)",
            r"create a file (.+)",
            r"ফাইল (.+) তৈরি করো",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                return create_text_file(
                    match.group(1).strip()
                )

        return None

    # =========================
    # File Search
    # =========================

    def file_search_intent(self, command):

        patterns = [
            r"find (.+)",
            r"find file (.+)",
            r"find folder (.+)",
            r"search file (.+)",
            r"search folder (.+)",
            r"search for (.+)",
            r"find my (.+)",
            r"খুঁজে দাও (.+)",
            r"খুঁজে দেখো (.+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                search_name = match.group(1).strip()

                return search_files(search_name)

        return None

    # =========================
    # File Information
    # =========================

    def file_info_intent(self, command):

        patterns = [
            r"file info (.+)",
            r"info about (.+)",
            r"information about (.+)",
            r"tell me about file (.+)",
            r"ফাইল (.+) এর তথ্য",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command
            )

            if match:

                return get_file_info(
                    match.group(1).strip()
                )

        return None

    # =========================
    # Main Intent Executor
    # =========================

    def remember_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "remember my ",
            "remember that my ",
            "remember ",
            "save my ",
            "save that my ",
            "save "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                content = text[len(prefix):].strip()

                if " is " not in content:
                    return "What should I remember?"

                key, value = content.split(
                    " is ",
                    1
                )

                key = key.strip()
                value = value.strip()

                if not key or not value:
                    return "Please provide both the information and its value."

                return self.memory.remember(
                    key,
                    value
                )
        return None

    def recall_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "what is my ",
            "what's my ",
            "where is my ",
            "tell me my ",
            "do you remember my ",
            "do you remember "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                key = text[len(prefix):].strip()

                if not key:
                    return "What should I look up?"

                value = self.memory.get(key)

                if value is None:
                    return f"I don't remember your {key}."

                return f"Your {key} is {value}."

        return None

    def recall_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "what is my ",
            "what's my ",
            "where is my ",
            "tell me my ",
            "do you remember my ",
            "do you remember "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                key = text[len(prefix):].strip()

                if not key:
                    return "What should I look up?"

                value = self.memory.get(key)

                if value is None:
                    return f"I don't remember your {key}."

                return f"Your {key} is {value}."

        return None

    def forget_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "forget my ",
            "forget ",
            "remove my ",
            "remove "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                key = text[len(prefix):].strip()

                key = key.replace(
                    " from memory",
                    ""
                ).strip()

                if not key:
                    return "What should I forget?"

                return self.memory.forget(key)

        return None

    def show_memory_intent(self, text):

        text = self.normalize(text)

        commands = [
            "show my memories",
            "show memories",
            "what do you remember",
            "what do you remember about me",
            "list my memories"
        ]

        if text in commands:

            memories = self.memory.all_memory()

            if not memories:
                return "I don't have anything saved in memory."

            result = "Here is what I remember:\n"

            for key, value in memories.items():

                result += f"- {key}: {value}\n"

            return result.strip()

        return None

    def rename_intent(self, text):

        text = self.normalize(text)

        if text.startswith("rename "):

            content = text[7:].strip()

            if " to " not in content:
                return "Please tell me the old name and new name."

            old_name, new_name = content.split(
                " to ",
                1
            )

            # return rename_item(
            #     old_name.strip(),
            #     new_name.strip()
            # )
            return self.confirmation.ask(
                f"rename {old_name} to {new_name}",
                lambda: rename_item(
                    old_name,
                    new_name
                )
            )

        return None

    def move_intent(self, text):

        text = self.normalize(text)

        pattern = r"move (.+) to (.+)"

        match = re.match(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            item_name = match.group(1).strip()
            destination_folder = match.group(2).strip()

            return self.confirmation.ask(
                f"move {item_name} to {destination_folder}",
                lambda: move_item(
                    item_name,
                    destination_folder
                )
            )

        return None

    def open_path_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "open path ",
            "open folder path ",
            "open file path "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                path = text[len(prefix):].strip()

                if not path:
                    return "Please provide the path."

                return open_path(path)

        return None

    def intelligent_memory_intent(self, text):

        text = text.strip()

        # Don't process normal memory commands here
        if text.lower().startswith((
            "remember my ",
            "remember that my ",
            "remember ",
            "save my ",
            "save that my ",
            "save "
        )):
            return None

        return self.memory.process(text)

    def delete_intent(self, text):

        text = self.normalize(text)

        patterns = [
            r"delete (.+)",
            r"remove (.+)",
            r"delete file (.+)",
            r"delete folder (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                item_name = match.group(1).strip()

                if not item_name:
                    return "What should I delete?"

                return self.confirmation.ask(
                    f"delete {item_name}",
                    lambda: delete_item(item_name)
                )

        return None

    def empty_recycle_bin_intent(self, text):

        text = self.normalize(text)

        commands = [
            "empty recycle bin",
            "clear recycle bin",
            "empty the recycle bin",
            "clear the recycle bin",
        ]

        if text in commands:

            return self.confirmation.ask(
                "permanently empty the Recycle Bin",
                empty_recycle_bin
            )

        return None

    def close_app_intent(self, text):

        text = self.normalize(text)

        prefixes = [
            "close ",
            "quit ",
            "exit "
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                app_name = text[len(prefix):].strip()

                if not app_name:
                    return "Which app should I close?"

                return self.confirmation.ask(
                    f"close {app_name}",
                    lambda: close_app(app_name)
                )

        return None

    def minimize_intent(self, text):

        text = self.normalize(text)

        commands = [
            "minimize all windows",
            "minimize all",
            "সব উইন্ডো মিনিমাইজ করো",
        ]

        if text in commands:

            return minimize_all_windows()

        return None

    def show_desktop_intent(self, text):

        text = self.normalize(text)

        commands = [
            "show desktop",
            "show my desktop",
            "desktop দেখাও",
        ]

        if text in commands:

            return show_desktop()

        return None

    def shutdown_intent(self, text):

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

    def restart_intent(self, text):

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

    def help_intent(self, text):

        text = self.normalize(text)

        help_commands = [
            "what can you do",
            "what can you do jarvis",
            "show commands",
            "show my commands",
            "list commands",
            "available commands",
            "help",
            "jarvis help",
            "কি কি করতে পারো",
            "তুমি কি করতে পারো",
            "কমান্ড দেখাও",
        ]

        if text not in help_commands:
            return None

        return """
            I can help you with these commands:

            Browser:
            - Open YouTube
            - Open Google
            - Search Google
            - Search YouTube

            Applications:
            - Open Notepad
            - Open Calculator
            - Open Chrome
            - Open VS Code
            - Close Chrome
            - Minimize all windows
            - Show desktop

            Files and folders:
            - Open Desktop
            - Open Downloads
            - Create a folder
            - Create a file
            - Search files
            - Rename a file
            - Move a file
            - Delete a file
            - Show recent files
            - Show file information

            Memory:
            - Remember that I live in Dhaka
            - What do you remember?
            - Forget my location

            System:
            - Shutdown PC
            - Restart PC
            - Stop listening
            - Bye

            You can also ask me normal questions using Gemini.
        """


    def smart_help_intent(self, command):

        # General help
        if command in [
            "help",
            "show commands",
            "list commands",
            "available commands",
            "what can you do",
            "what do you do",
            "what can you do jarvis",
            "কি কি করতে পারো",
            "তুমি কি করতে পারো",
            "কমান্ড দেখাও",
        ]:

            return self.help_intent(command)

        # File-related help
        if any(keyword in command for keyword in [
            "what can you do with file",
            "what can you do with files",
            "what can you do with folder",
            "what can you do with folders",
            "file related commands",
            "folder related commands",
            "ফাইল দিয়ে কি করতে পারো",
            "ফোল্ডার দিয়ে কি করতে পারো",
        ]):

            return """
            For files and folders, I can:

            - Create a folder
            - Create a file
            - Search files
            - Open a file or folder
            - Rename a file
            - Move a file
            - Delete a file
            - Show recent files
            - Show file information
            """

        # Application-related help
        if any(keyword in command for keyword in [
            "what can you do with app",
            "what can you do with application",
            "what can you do with software",
            "app related commands",
            "application related commands",
            "অ্যাপ দিয়ে কি করতে পারো",
        ]):

            return """
                For applications, I can:

                - Open Notepad
                - Open Calculator
                - Open Chrome
                - Open VS Code
                - Open CMD
                - Close applications
                - Minimize all windows
                - Show desktop
                """

        # Memory-related help
        if any(keyword in command for keyword in [
            "what can you do with memory",
            "memory related commands",
            "what can you remember",
            "মেমোরি দিয়ে কি করতে পারো",
        ]):

            return """
                For memory, I can:

                - Remember information
                - Recall information
                - Show saved memories
                - Forget saved information
                """

        # System-related help
        if any(keyword in command for keyword in [
            "what can you do with system",
            "system related commands",
            "what can you do with computer",
            "computer related commands",
            "সিস্টেম দিয়ে কি করতে পারো",
        ]):

            return """
                For system control, I can:

                - Shutdown the PC
                - Restart the PC
                - Stop listening
                - Exit JARVIS
                """

        return None

    


    # Execute
    def execute(self, command):

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

        memory_result = self.memory.process(command)
        
        if memory_result:
            return memory_result
        

        # Smart help
        result = self.smart_help_intent(command)

        if result:
            return result

        # =========================
        # DYNAMIC ACTIONS
        # =========================

        result = self.google_search_intent(command)
        if result:
            return result

        result = self.youtube_search_intent(command)
        if result:
            return result

        result = self.create_folder_intent(command)
        if result:
            return result

        result = self.create_file_intent(command)
        if result:
            return result

        result = self.file_info_intent(command)
        if result:
            return result

        result = self.file_search_intent(command)
        if result:
            return result

        result = self.rename_intent(command)
        if result:
            return result

        result = self.empty_recycle_bin_intent(command)

        if result:
            return result
        
        result = self.delete_intent(command)

        if result:
            return result

        result = self.move_intent(command)
        if result:
            return result

        result = self.open_path_intent(command)
        if result:
            return result

        result = self.close_app_intent(command)

        if result:
            return result

        result = self.shutdown_intent(command)

        if result:
            return result

        result = self.restart_intent(command)

        if result:
            return result

        result = self.minimize_intent(command)

        if result:
            return result

        result = self.show_desktop_intent(command)

        if result:
            return result

        # =========================
        # MEMORY
        # =========================

        result = self.remember_intent(command)
        if result:
            return result

        result = self.recall_intent(command)
        if result:
            return result

        result = self.forget_intent(command)
        if result:
            return result

        result = self.show_memory_intent(command)
        if result:
            return result

        result = self.intelligent_memory_intent(command)
        if result:
            return result



        # Volume control
        if command in [
            "what is the volume",
            "check volume",
            "get volume",
            "volume status",
            "আমার ভলিউম কত"
        ]:
            return get_volume()

        if command in [
            "increase volume",
            "volume up",
            "turn up volume",
            "ভলিউম বাড়াও"
        ]:
            return increase_volume()

        if command in [
            "decrease volume",
            "volume down",
            "turn down volume",
            "ভলিউম কমাও"
        ]:
            return decrease_volume()

        if command in [
            "mute volume",
            "mute",
            "ভলিউম বন্ধ করো"
        ]:
            return mute_volume()

        if command in [
            "unmute volume",
            "unmute",
            "ভলিউম চালু করো"
        ]:
            return unmute_volume()

        if command.startswith("set volume "):
            level = command.replace(
                "set volume ",
                "",
                1
            ).replace("%", "").strip()

            return set_volume(level)

        if command.startswith("volume "):
            level = command.replace(
                "volume ",
                "",
                1
            ).replace("%", "").strip()

            if level.isdigit():
                return set_volume(level)
            
        # =========================
        # RECENT FILES
        # =========================

        if command in [
            "recent files",
            "show recent files",
            "my recent files",
            "open recent files",
        ]:

            return get_recent_files()


        if command.startswith("weather in "):

            city = command.replace("weather in ", "").strip()

            if city:
                return get_weather(city)

            return get_weather("Dhaka")

        if command.startswith("open website "):

            url = command.replace("open website ", "").strip()

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            return open_website(url)

        if command.startswith("latest news about "):

            query = command.replace("latest news about ", "").strip()

            if query:
                return news_search(query)

            return "What news should I search for?"

        
        # =========================
        # NORMAL COMMANDS
        # =========================

        for intent, data in self.commands.items():

            for keyword in data["keywords"]:

                if keyword in command:

                    return data["function"]()


        return None

    