import re

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


class BrowserIntents:

    def __init__(self):
        pass

    # =========================
    # Google Search
    # =========================

    def google_search(self, command):

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

            match = re.search(pattern, command, re.IGNORECASE)

            if match:

                query = match.group(1).strip()

                query = re.sub(
                    r"\s+(search|khojo|khuj|করো|দাও)$",
                    "",
                    query,
                    flags=re.IGNORECASE
                )

                return search_google(query)

        return None

    # =========================
    # YouTube Search
    # =========================

    def youtube_search(self, command):

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

            match = re.search(pattern, command, re.IGNORECASE)

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
    # Open Websites
    # =========================

    def open_youtube(self, text):
        if text == "open youtube":
            return open_youtube()

        return None

    def open_google(self, text):
        if text == "open google":
            return open_google()

        return None

    def open_github(self, text):
        if text == "open github":
            return open_github()

        return None

        # =========================
    # Weather
    # =========================

    def weather(self, command):

        if command.startswith("weather in "):

            city = command.replace(
                "weather in ",
                "",
                1
            ).strip()

            if city:
                return get_weather(city)

            return get_weather("Dhaka")

        return None

    # =========================
    # Open Website
    # =========================

    def open_website(self, command):

        if command.startswith("open website "):

            url = command.replace(
                "open website ",
                "",
                1
            ).strip()

            if not url:
                return "Please provide a website."

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            return open_website(url)

        return None

    # =========================
    # News Search
    # =========================

    def news(self, command):

        if command.startswith("latest news about "):

            query = command.replace(
                "latest news about ",
                "",
                1
            ).strip()

            if query:
                return news_search(query)

            return "What news should I search for?"

        return None



    # =========================
    # Main Execute
    # =========================

    def execute(self, command):

        result = self.google_search(command)

        if result is not None:
            return result

        result = self.youtube_search(command)

        if result is not None:
            return result

        result = self.open_youtube(command)

        if result is not None:
            return result

        result = self.open_google(command)

        if result is not None:
            return result

        result = self.open_github(command)

        if result is not None:
            return result

        result = self.weather(command)

        if result is not None:
            return result

        result = self.open_website(command)

        if result is not None:
            return result

        result = self.news(command)

        if result is not None:
            return result

        return None