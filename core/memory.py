
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

        os.makedirs(
            self.memory_dir,
            exist_ok=True
        )

        if not os.path.exists(self.memory_file):
            self._save({})

    # =====================================================
    # LOAD / SAVE
    # =====================================================

    def _load(self):

        try:

            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return data if isinstance(data, dict) else {}

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return {}

    def _save(self, data):

        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # REMEMBER
    # =====================================================

    def remember(self, key, value):

        data = self._load()

        key = key.strip().lower()
        value = value.strip()

        if not key or not value:
            return "I could not save that memory."

        data[key] = value

        self._save(data)

        return (
            f"I'll remember that your "
            f"{key} is {value}."
        )

    # =====================================================
    # RECALL
    # =====================================================

    def recall(self, key):

        data = self._load()

        key = key.strip().lower()

        if key in data:

            return (
                f"Your {key} is "
                f"{data[key]}."
            )

        return (
            f"I don't remember your "
            f"{key}."
        )

    # =====================================================
    # FORGET
    # =====================================================

    def forget(self, key):

        data = self._load()

        key = key.strip().lower()

        if key in data:

            del data[key]

            self._save(data)

            return (
                f"I forgot your "
                f"{key}."
            )

        return (
            f"I don't have any memory "
            f"about your {key}."
        )

    # =====================================================
    # SHOW ALL
    # =====================================================

    def show_all(self):

        data = self._load()

        if not data:

            return (
                "I don't have any saved "
                "memories yet."
            )

        result = [
            "Here is what I remember about you:"
        ]

        for key, value in data.items():

            result.append(
                f"- Your {key} is {value}"
            )

        return "\n".join(result)

    # =====================================================
    # CLEAR ALL
    # =====================================================

    def clear_all(self):

        self._save({})

        return "All memories have been cleared."

    # =====================================================
    # EXTRACT MEMORY
    # =====================================================

    def extract_memory(self, text):

        command = text.strip()

        # -------------------------------------------------
        # My name is Tarek
        # -------------------------------------------------

        match = re.search(
            r"^(?:my name is|remember my name is|remember my name)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "name", value

        # -------------------------------------------------
        # I live in Dhaka
        # -------------------------------------------------

        match = re.search(
            r"^(?:i live in|my location is|remember i live in)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "location", value

        # -------------------------------------------------
        # My job is Laravel developer
        # -------------------------------------------------

        match = re.search(
            r"^(?:my job is|i work as|my profession is)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "job", value

        # -------------------------------------------------
        # Favorite programming language
        # -------------------------------------------------

        match = re.search(
            r"^(?:my favorite programming language is|my favorite language is)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "favorite programming language", value

        # -------------------------------------------------
        # I like Python
        # -------------------------------------------------

        match = re.search(
            r"^i like\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "likes", value

        # -------------------------------------------------
        # I love anime
        # -------------------------------------------------

        match = re.search(
            r"^i love\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "loves", value

        # -------------------------------------------------
        # I am learning Laravel
        # -------------------------------------------------

        match = re.search(
            r"^(?:i am learning|i'm learning|i learn)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "learning", value

        # -------------------------------------------------
        # I prefer VS Code
        # -------------------------------------------------

        match = re.search(
            r"^(?:i prefer|my preferred)\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "preference", value

        # -------------------------------------------------
        # My favorite editor is VS Code
        # -------------------------------------------------

        match = re.search(
            r"^my favorite editor is\s+(.+)$",
            command,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if value:

                return "favorite editor", value

        return None

    # =====================================================
    # PROCESS
    # =====================================================

    def process(self, text):

        command = text.lower().strip()

        # -------------------------------------------------
        # Save memory
        # -------------------------------------------------

        extracted = self.extract_memory(text)

        if extracted:

            key, value = extracted

            return self.remember(
                key,
                value
            )

        # -------------------------------------------------
        # Explicit remember command
        # -------------------------------------------------

        if command.startswith("remember "):

            value = text[9:].strip()

            if value:

                return (
                    "What should I remember? "
                    "You can say: my name is Tarek."
                )

        # -------------------------------------------------
        # Recall name
        # -------------------------------------------------

        if command in [
            "what is my name",
            "what's my name",
            "who am i",
            "do you remember my name"
        ]:

            return self.recall("name")

        # -------------------------------------------------
        # Recall location
        # -------------------------------------------------

        if command in [
            "where do i live",
            "what is my location",
            "where am i from"
        ]:

            return self.recall("location")

        # -------------------------------------------------
        # Recall job
        # -------------------------------------------------

        if command in [
            "what is my job",
            "what do i do",
            "what is my profession"
        ]:

            return self.recall("job")

        # -------------------------------------------------
        # Recall favorite language
        # -------------------------------------------------

        if command in [
            "what is my favorite language",
            "what is my favorite programming language"
        ]:

            return self.recall(
                "favorite programming language"
            )

        # -------------------------------------------------
        # Recall likes
        # -------------------------------------------------

        if command in [
            "what do i like",
            "what are my likes",
            "what do you know i like"
        ]:

            return self.recall("likes")

        # -------------------------------------------------
        # Recall learning
        # -------------------------------------------------

        if command in [
            "what am i learning",
            "what do i learn",
            "what am i currently learning"
        ]:

            return self.recall("learning")

        # -------------------------------------------------
        # Recall preference
        # -------------------------------------------------

        if command in [
            "what do i prefer",
            "what are my preferences",
            "what is my preference"
        ]:

            return self.recall("preference")

        # -------------------------------------------------
        # Recall favorite editor
        # -------------------------------------------------

        if command in [
            "what is my favorite editor",
            "which editor do i like"
        ]:

            return self.recall("favorite editor")

        # -------------------------------------------------
        # Show all memory
        # -------------------------------------------------

        if command in [
            "what do you remember about me",
            "show my memory",
            "show memories",
            "what do you know about me"
        ]:

            return self.show_all()

        # -------------------------------------------------
        # Forget memory
        # -------------------------------------------------

        if command.startswith("forget my "):

            key = command.replace(
                "forget my ",
                "",
                1
            ).strip()

            return self.forget(key)

        # -------------------------------------------------
        # Clear all memory
        # -------------------------------------------------

        if command in [
            "forget everything",
            "clear memory",
            "clear all memory",
            "delete all memories"
        ]:

            return self.clear_all()

        return None

    # =====================================================
    # BACKWARD COMPATIBILITY
    # =====================================================

    def remember_sentence(self, text):

        result = self.extract_memory(text)

        if result:

            key, value = result

            return self.remember(
                key,
                value
            )

        return "What should I remember?"
