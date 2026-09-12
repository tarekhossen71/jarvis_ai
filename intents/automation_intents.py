import re

from tools.browser_tools import (
    open_google,
    search_google,
    open_youtube,
    search_youtube,
)


class AutomationIntents:

    def __init__(self):
        pass

    # =========================
    # YouTube Automation
    # =========================

    def youtube_automation(self, command):

        patterns = [
            r"open youtube and search (.+)",
            r"open youtube then search (.+)",
            r"youtube open kore (.+) search",
            r"ইউটিউব ওপেন করে (.+) সার্চ",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command,
                re.IGNORECASE
            )

            if match:

                query = match.group(1).strip()

                if not query:
                    return "Please provide a search query."

                # search_youtube() নিজেই YouTube search URL open করে
                search_result = search_youtube(query)

                return (
                    f"YouTube opened with search results for {query}."
                )

        return None

    # =========================
    # Google Automation
    # =========================

    def google_automation(self, command):

        patterns = [
            r"open google and search (.+)",
            r"open google then search (.+)",
            r"google open kore (.+) search",
            r"গুগল ওপেন করে (.+) সার্চ",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                command,
                re.IGNORECASE
            )

            if match:

                query = match.group(1).strip()

                if not query:
                    return "Please provide a search query."

                # search_google() নিজেই Google search URL open করে
                search_result = search_google(query)

                return (
                    f"Google opened with search results for {query}."
                )

        return None

    # =========================
    # Main Execute
    # =========================

    def execute(self, command):

        result = self.youtube_automation(command)

        if result is not None:
            return result

        result = self.google_automation(command)

        if result is not None:
            return result

        return None