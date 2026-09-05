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

                if " is " not in content:
                    return "What should I remember?"

                key, value = content.split(" is ", 1)

                key = key.strip()
                value = value.strip()

                if not key or not value:
                    return "Please provide both the information and its value."

                return self.memory.remember(key, value)

        return None

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