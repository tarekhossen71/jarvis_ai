import re
from tools.browser_tools import search_youtube

class MultiStepIntents:

    def __init__(self, intent_manager):
        self.intent_manager = intent_manager

    def split_commands(self, command):

        # Split only when "and / then / and then" is used
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

    def normalize_step(self, part, index):

        part = part.strip()

        if not part:
            return None

        # -----------------------------------------
        # Known applications
        # -----------------------------------------

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

        # -----------------------------------------
        # Example:
        # open notepad and calculator
        #
        # Step 1:
        # open notepad
        #
        # Step 2:
        # calculator
        #
        # Convert step 2 -> open calculator
        # -----------------------------------------

        if index > 1:

            if not re.match(
                r"^(open|launch|start|close|exit|quit)\s+",
                part,
                re.IGNORECASE
            ):

                if part.lower() in known_apps:
                    part = f"open {part}"

        return part

    def execute(self, command):

        parts = self.split_commands(command)

        # Single command হলে Multi-Step নয়
        if len(parts) < 2:
            return None

        results = []

        # Browser context
        active_browser = None

        for index, part in enumerate(parts, start=1):

            part = self.normalize_step(part, index)

            if not part:
                continue

            print(f"🔹 Step {index}: {part}")

            # =========================================
            # Detect browser from previous step
            # =========================================

            if re.fullmatch(
                r"open (chrome|google chrome)",
                part,
                re.IGNORECASE
            ):
                active_browser = "chrome"

            elif re.fullmatch(
                r"open firefox",
                part,
                re.IGNORECASE
            ):
                active_browser = "firefox"

            # =========================================
            # YouTube search with browser context
            # =========================================

            youtube_match = re.fullmatch(
                r"search youtube for (.+)",
                part,
                re.IGNORECASE
            )

            if youtube_match and active_browser:

                query = youtube_match.group(1).strip()

                result = search_youtube(
                    query,
                    browser=active_browser
                )

            else:

                # =====================================
                # Normal intent execution
                # =====================================

                result = self.intent_manager.execute_single(part)

            # =========================================
            # Step failed
            # =========================================

            if not result:

                return (
                    f"Workflow stopped at step {index}: "
                    f"I couldn't execute '{part}'."
                )

            results.append(str(result))

        return " ".join(results)