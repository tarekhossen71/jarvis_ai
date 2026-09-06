
import re


class MultiStepIntents:

    def __init__(self, intent_manager):
        self.intent_manager = intent_manager

    def split_commands(self, command):

        # Examples:
        # open notepad and open calculator
        # open notepad then open calculator
        # open notepad and then open calculator
        # open notepad and calculator

        parts = re.split(
            r"\s+(?:and then|then|and)\s+",
            command,
            flags=re.IGNORECASE
        )

        return [
            part.strip()
            for part in parts
            if part.strip()
        ]

    def execute(self, command):

        parts = self.split_commands(command)

        # Single command হলে Multi-Step নয়
        if len(parts) < 2:
            return None

        results = []

        for index, part in enumerate(parts, start=1):

            # -----------------------------------------
            # Handle app names without "open"
            # -----------------------------------------
            #
            # Example:
            # open notepad and calculator
            #
            # becomes:
            # open notepad
            # open calculator
            #
            if index > 1 and not re.match(
                r"^(open|launch|start|close|exit|quit)\s+",
                part,
                re.IGNORECASE
            ):

                known_apps = [
                    "notepad",
                    "note pad",
                    "calculator",
                    "calc",
                    "explorer",
                    "file explorer",
                    "command prompt",
                    "cmd",
                    "powershell",
                    "power shell",
                    "vscode",
                    "vs code",
                    "visual studio code",
                    "chrome",
                    "google chrome",
                ]

                if part.lower() in known_apps:
                    part = f"open {part}"

            # -----------------------------------------
            # Execute Step
            # -----------------------------------------

            result = self.intent_manager.execute_single(part)

            # Step failed
            if not result:

                return (
                    f"Workflow stopped at step {index}: "
                    f"I couldn't execute '{part}'."
                )

            results.append(result)

        return " ".join(results)
