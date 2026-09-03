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

    def _load(self):
        try:
            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
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

    def remember(self, key, value):
        data = self._load()

        data[key] = value.strip()

        self._save(data)

        return f"I'll remember that your {key} is {value.strip()}."

    def recall(self, key):
        data = self._load()

        if key in data:
            return f"Your {key} is {data[key]}."

        return f"I don't remember your {key}."

    def forget(self, key):
        data = self._load()

        if key in data:
            del data[key]
            self._save(data)

            return f"I forgot your {key}."

        return f"I don't have any memory about your {key}."

    def show_all(self):
        data = self._load()

        if not data:
            return "I don't have any saved memories yet."

        result = ["Here is what I remember about you:"]

        for key, value in data.items():
            result.append(f"- Your {key} is {value}")

        return "\n".join(result)

    def clear_all(self):
        self._save({})

        return "All memories have been cleared."

    def extract_memory(self, text):
        command = text.lower().strip()

        # My name is Tarek
        match = re.search(
            r"(?:my name is|remember my name is|remember my name)\s+(.+)",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "name", value

        # I live in Dhaka / My location is Dhaka
        match = re.search(
            r"(?:i live in|my location is|remember i live in)\s+(.+)",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "location", value

        # My job is Laravel developer
        match = re.search(
            r"(?:my job is|i work as|my profession is)\s+(.+)",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "job", value

        # My favorite programming language is PHP
        match = re.search(
            r"(?:my favorite programming language is|my favorite language is)\s+(.+)",
            command,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            if value:
                return "favorite programming language", value

        return None

    def process(self, text):
        command = text.lower().strip()

        # Save memory
        extracted = self.extract_memory(text)

        if extracted:
            key, value = extracted
            return self.remember(key, value)

        # Explicit remember command
        if command.startswith("remember "):
            value = text[9:].strip()

            if value:
                return (
                    "What should I remember? "
                    "You can say: my name is Tarek."
                )

        # Recall name
        if command in [
            "what is my name",
            "what's my name",
            "who am i",
            "do you remember my name"
        ]:
            return self.recall("name")

        # Recall location
        if command in [
            "where do i live",
            "what is my location",
            "where am i from"
        ]:
            return self.recall("location")

        # Recall job
        if command in [
            "what is my job",
            "what do i do",
            "what is my profession"
        ]:
            return self.recall("job")

        # Recall favorite language
        if command in [
            "what is my favorite language",
            "what is my favorite programming language"
        ]:
            return self.recall("favorite programming language")

        # Show all memory
        if command in [
            "what do you remember about me",
            "show my memory",
            "show memories",
            "what do you know about me"
        ]:
            return self.show_all()

        # Forget memory
        if command.startswith("forget my "):
            key = command.replace("forget my ", "", 1).strip()

            return self.forget(key)

        # Clear all memory
        if command in [
            "forget everything",
            "clear memory",
            "clear all memory",
            "delete all memories"
        ]:
            return self.clear_all()

        return None

    def remember_sentence(self, text):
        """
        Backward-compatible method.
        Old intent.py code uses this method.
        """

        result = self.extract_memory(text)

        if result:
            key, value = result
            return self.remember(key, value)

        return "What should I remember?"