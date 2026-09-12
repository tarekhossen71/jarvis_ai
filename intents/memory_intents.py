
import re


class MemoryIntents:

    def __init__(self, memory):
        self.memory = memory

    # =====================================================
    # NORMALIZE
    # =====================================================

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

            text = text.replace(
                word,
                " "
            )

        return " ".join(text.split())

    # =====================================================
    # REMEMBER
    # =====================================================

    def remember(self, text):

        original_text = text.strip()

        text = self.normalize(text)

        # -------------------------------------------------
        # Supported prefixes
        # -------------------------------------------------

        prefixes = [
            "remember that my ",
            "remember my ",
            "remember that ",
            "remember ",
            "save that my ",
            "save my ",
            "save that ",
            "save ",
        ]

        content = None

        for prefix in prefixes:

            if text.startswith(prefix):

                content = text[
                    len(prefix):
                ].strip()

                break

        if content is None:

            return None

        # -------------------------------------------------
        # Remove optional "my"
        # -------------------------------------------------

        if content.startswith("my "):

            content = content[3:].strip()

        # -------------------------------------------------
        # Must contain "is"
        # -------------------------------------------------

        if " is " not in content:

            return (
                "What should I remember? "
                "You can say: my name is Tarek."
            )

        # -------------------------------------------------
        # Split key/value
        # -------------------------------------------------

        key, value = content.split(
            " is ",
            1
        )

        key = key.strip()
        value = value.strip()

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not key or not value:

            return (
                "Please provide both "
                "the information and its value."
            )

        # -------------------------------------------------
        # Preserve Windows paths
        #
        # normalize() only affects command text.
        # The value itself is already extracted.
        # -------------------------------------------------

        value = value.rstrip(".")

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        return self.memory.remember(
            key,
            value
        )

    # =====================================================
    # RECALL
    # =====================================================

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

                key = text[
                    len(prefix):
                ].strip()

                # Remove unnecessary suffix
                key = re.sub(
                    r"\s+from memory$",
                    "",
                    key,
                    flags=re.IGNORECASE
                ).strip()

                if not key:

                    return "What should I look up?"

                value = self.memory.get(key)

                if value is None:

                    return (
                        f"I don't remember "
                        f"your {key}."
                    )

                return (
                    f"Your {key} is "
                    f"{value}."
                )

        return None

    # =====================================================
    # FORGET
    # =====================================================

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

                key = text[
                    len(prefix):
                ].strip()

                key = key.replace(
                    " from memory",
                    ""
                ).strip()

                if not key:

                    return "What should I forget?"

                return self.memory.forget(key)

        return None

    # =====================================================
    # SHOW ALL MEMORY
    # =====================================================

    def show(self, text):

        text = self.normalize(text)

        commands = [
            "show my memories",
            "show memories",
            "show my memory",
            "what do you remember",
            "what do you remember about me",
            "what do you know about me",
            "list my memories",
        ]

        if text not in commands:

            return None

        memories = self.memory.all_memory()

        if not memories:

            return (
                "I don't have anything "
                "saved in memory."
            )

        result = [
            "Here is what I remember:"
        ]

        for key, value in memories.items():

            result.append(
                f"- {key}: {value}"
            )

        return "\n".join(result)

    # =====================================================
    # PROCESS
    # =====================================================

    def process(self, text):

        # -------------------------------------------------
        # Remember
        # -------------------------------------------------

        result = self.remember(text)

        if result is not None:

            return result

        # -------------------------------------------------
        # Recall
        # -------------------------------------------------

        result = self.recall(text)

        if result is not None:

            return result

        # -------------------------------------------------
        # Forget
        # -------------------------------------------------

        result = self.forget(text)

        if result is not None:

            return result

        # -------------------------------------------------
        # Show memory
        # -------------------------------------------------

        result = self.show(text)

        if result is not None:

            return result

        return None
