import json
import os
import re


class MemoryManager:

    def __init__(self):
        self.memory_dir = "memory"
        self.memory_file = os.path.join(
            self.memory_dir,
            "memory.json"
        )

        os.makedirs(self.memory_dir, exist_ok=True)

        if not os.path.exists(self.memory_file):
            self._save({})

    # =========================================================
    # LOAD / SAVE
    # =========================================================

    def _load(self):
        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, dict):
                    return data

                return {}

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save(self, data):
        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =========================================================
    # BASIC MEMORY OPERATIONS
    # =========================================================

    def remember(self, key, value):
        data = self._load()

        key = str(key).strip().lower()
        value = str(value).strip()

        if not key or not value:
            return "I could not save that memory."

        data[key] = value

        self._save(data)

        return f"I'll remember that your {key} is {value}."

    def get(self, key):
        """
        Dynamically get any saved memory.

        Example:
            get("project folder")
            get("work folder")
            get("favorite editor")
        """

        data = self._load()

        key = str(key).strip().lower()

        if key in data:
            return data[key]

        return None

    def recall(self, key):
        key = str(key).strip().lower()

        value = self.get(key)

        if value is not None:
            return f"Your {key} is {value}."

        return f"I don't remember your {key}."

    def forget(self, key):
        data = self._load()

        key = str(key).strip().lower()

        if key in data:
            del data[key]

            self._save(data)

            return f"I forgot your {key}."

        return f"I don't have any memory about your {key}."

    def all_memory(self):
        return self._load()

    def show_all(self):
        data = self._load()

        if not data:
            return "I don't have any saved memories yet."

        result = [
            "Here is what I remember about you:"
        ]

        for key, value in data.items():
            result.append(
                f"- Your {key} is {value}"
            )

        return "\n".join(result)

    def clear_all(self):
        self._save({})

        return "All memories have been cleared."

    # =========================================================
    # DYNAMIC MEMORY EXTRACTION
    # =========================================================

    def extract_memory(self, text):

        command = text.strip()

        # -----------------------------------------------------
        # "my name is Tarek"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:remember\s+)?my\s+name\s+is\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "name", value

        # -----------------------------------------------------
        # "i live in Dhaka"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:remember\s+)?(?:i\s+live\s+in|my\s+location\s+is)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "location", value

        # -----------------------------------------------------
        # "my job is Laravel developer"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:remember\s+)?(?:my\s+job\s+is|i\s+work\s+as|my\s+profession\s+is)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "job", value

        # -----------------------------------------------------
        # "my favorite programming language is PHP"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:remember\s+)?my\s+favorite\s+programming\s+language\s+is\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "favorite programming language", value

        # -----------------------------------------------------
        # "i like Python"
        # -----------------------------------------------------

        match = re.search(
            r"^i\s+like\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "likes", value

        # -----------------------------------------------------
        # "i love Python"
        # -----------------------------------------------------

        match = re.search(
            r"^i\s+love\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "loves", value

        # -----------------------------------------------------
        # "i am learning Python"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:i\s+am\s+learning|i'm\s+learning|i\s+learn)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "learning", value

        # -----------------------------------------------------
        # "i prefer VS Code"
        # -----------------------------------------------------

        match = re.search(
            r"^(?:i\s+prefer|my\s+preferred)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "preference", value

        # -----------------------------------------------------
        # "my favorite editor is VS Code"
        # -----------------------------------------------------

        match = re.search(
            r"^my\s+favorite\s+editor\s+is\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "favorite editor", value

        # -----------------------------------------------------
        # DYNAMIC:
        #
        # remember my project folder D:\Tarek\Projects
        #
        # remember my work folder D:\Tarek\Projects
        #
        # remember my office PC Tarek-PC
        #
        # remember my github username tarek_dev
        #
        # No static key list.
        # -----------------------------------------------------

        match = re.search(
            r"^remember\s+(?:that\s+)?my\s+(.+?)\s+(?:is|=)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            key = match.group(1).strip()
            value = match.group(2).strip()

            if key and value:
                return key, value

        # -----------------------------------------------------
        # Dynamic:
        #
        # remember project folder is D:\Tarek\Projects
        # remember office = Dhaka
        # -----------------------------------------------------

        match = re.search(
            r"^remember\s+(.+?)\s+(?:is|=)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            key = match.group(1).strip()
            value = match.group(2).strip()

            # Avoid treating generic sentences as memory
            if key and value:
                return key, value

        # -----------------------------------------------------
        # Dynamic:
        #
        # remember my project folder D:\Tarek\Projects
        #
        # IMPORTANT:
        # This supports values without "is".
        #
        # Path detection is used here so Windows paths work.
        # -----------------------------------------------------

        match = re.search(
            r"^remember\s+(?:that\s+)?my\s+(.+?)\s+((?:[a-zA-Z]:\\|[a-zA-Z]:/).+)$",
            command,
            re.IGNORECASE
        )

        if match:

            key = match.group(1).strip()
            value = match.group(2).strip()

            if key and value:
                return key, value

        return None

    # =========================================================
    # PROCESS MEMORY COMMANDS
    # =========================================================

    def process(self, text):

        original_text = text.strip()
        command = original_text.lower().strip()

        # -----------------------------------------------------
        # SAVE MEMORY
        # -----------------------------------------------------

        extracted = self.extract_memory(original_text)

        if extracted:

            key, value = extracted

            return self.remember(key, value)

        # -----------------------------------------------------
        # DYNAMIC RECALL
        #
        # what is my project folder
        # what is my work folder
        # what is my github username
        # where is my project folder
        # tell me my project folder
        #
        # No static key list.
        # -----------------------------------------------------

        recall_patterns = [
            r"^what\s+is\s+my\s+(.+)$",
            r"^what's\s+my\s+(.+)$",
            r"^where\s+is\s+my\s+(.+)$",
            r"^tell\s+me\s+my\s+(.+)$",
            r"^do\s+you\s+remember\s+my\s+(.+)$",
            r"^do\s+you\s+remember\s+(.+)$",
        ]

        for pattern in recall_patterns:

            match = re.match(
                pattern,
                command,
                re.IGNORECASE
            )

            if match:

                key = match.group(1).strip()

                if not key:
                    return "What should I look up?"

                # Remove common trailing words
                key = re.sub(
                    r"\s+from\s+memory$",
                    "",
                    key,
                    flags=re.IGNORECASE
                ).strip()

                return self.recall(key)

        # -----------------------------------------------------
        # SHOW ALL MEMORY
        # -----------------------------------------------------

        show_commands = [
            "what do you remember about me",
            "what do you remember",
            "show my memory",
            "show memories",
            "show my memories",
            "list my memories",
            "what do you know about me",
        ]

        if command in show_commands:
            return self.show_all()

        # -----------------------------------------------------
        # DYNAMIC FORGET
        #
        # forget my project folder
        # forget my work folder
        # forget my github username
        # -----------------------------------------------------

        forget_match = re.match(
            r"^forget\s+(?:my\s+)?(.+)$",
            command,
            re.IGNORECASE
        )

        if forget_match:

            key = forget_match.group(1).strip()

            key = re.sub(
                r"\s+from\s+memory$",
                "",
                key,
                flags=re.IGNORECASE
            ).strip()

            if key:
                return self.forget(key)

        # -----------------------------------------------------
        # CLEAR ALL MEMORY
        # -----------------------------------------------------

        clear_commands = [
            "forget everything",
            "clear memory",
            "clear all memory",
            "delete all memories",
            "clear memories",
        ]

        if command in clear_commands:
            return self.clear_all()

        return None

    # =========================================================
    # COMPATIBILITY METHOD
    # =========================================================

    def remember_sentence(self, text):

        result = self.extract_memory(text)

        if result:

            key, value = result

            return self.remember(key, value)

        return "What should I remember?"


# =============================================================
# MEMORY INTENTS
# =============================================================

class MemoryIntents:

    def __init__(self, memory):
        self.memory = memory

    def normalize(self, text):

        text = text.lower().strip()

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

        return " ".join(text.split())

    # ---------------------------------------------------------
    # REMEMBER
    # ---------------------------------------------------------

    def remember(self, text):

        text = self.normalize(text)

        prefixes = [
            "remember my ",
            "remember that my ",
            "remember ",
            "save my ",
            "save that my ",
            "save ",
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                content = text[len(prefix):].strip()

                # First try "key is value"
                if " is " in content:

                    key, value = content.split(
                        " is ",
                        1
                    )

                # Also support "="
                elif "=" in content:

                    key, value = content.split(
                        "=",
                        1
                    )

                else:

                    # Windows path without "is"
                    path_match = re.match(
                        r"^(.+?)\s+((?:[a-zA-Z]:\\|[a-zA-Z]:/).+)$",
                        content
                    )

                    if path_match:

                        key = path_match.group(1)
                        value = path_match.group(2)

                    else:
                        return "What should I remember?"

                key = key.strip()
                value = value.strip()

                if not key or not value:
                    return (
                        "Please provide both "
                        "the information and its value."
                    )

                return self.memory.remember(
                    key,
                    value
                )

        return None

    # ---------------------------------------------------------
    # DYNAMIC RECALL
    # ---------------------------------------------------------

    def recall(self, text):

        text = self.normalize(text)

        prefixes = [
            "what is my ",
            "what's my ",
            "where is my ",
            "tell me my ",
            "do you remember my ",
            "do you remember ",
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

    # ---------------------------------------------------------
    # DYNAMIC FORGET
    # ---------------------------------------------------------

    def forget(self, text):

        text = self.normalize(text)

        prefixes = [
            "forget my ",
            "forget ",
            "remove my ",
            "remove ",
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

    # ---------------------------------------------------------
    # SHOW
    # ---------------------------------------------------------

    def show(self, text):

        text = self.normalize(text)

        commands = [
            "show my memories",
            "show memories",
            "what do you remember",
            "what do you remember about me",
            "list my memories",
        ]

        if text not in commands:
            return None

        memories = self.memory.all_memory()

        if not memories:
            return "I don't have anything saved in memory."

        result = "Here is what I remember:\n"

        for key, value in memories.items():

            result += f"- {key}: {value}\n"

        return result.strip()