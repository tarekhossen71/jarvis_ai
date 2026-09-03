import webbrowser
from urllib.parse import quote
import requests

def open_youtube():

    webbrowser.open(
        "https://www.youtube.com"
    )

    return "Opening YouTube."


def open_google():

    webbrowser.open(
        "https://www.google.com"
    )

    return "Opening Google."


def open_github():

    webbrowser.open(
        "https://github.com"
    )

    return "Opening GitHub."


def search_google(query):

    query = query.strip()

    if not query:
        return "What should I search for?"

    url = (
        "https://www.google.com/search?q="
        + quote(query)
    )

    webbrowser.open(url)

    return f"Searching Google for {query}."


def search_youtube(query):

    query = query.strip()

    if not query:
        return "What should I search for on YouTube?"

    url = (
        "https://www.youtube.com/results?search_query="
        + quote(query)
    )

    webbrowser.open(url)

    return f"Searching YouTube for {query}."

def open_website(url):

    try:
        webbrowser.open(url)

        return f"Opening {url}"

    except Exception as e:

        return f"Could not open website: {str(e)}"


def get_weather(city="Dhaka"):

    try:
        url = (
            f"https://wttr.in/{city}"
            "?format=%C+%t+FeelsLike:%f+Humidity:%h"
        )

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"

        return "Sorry, I could not get the weather information."

    except requests.RequestException:
        return "Weather service is currently unavailable."

def news_search(query):

    url = (
        "https://www.google.com/search?"
        f"q={query.replace(' ', '+')}&tbm=nws"
    )

    webbrowser.open(url)

    return f"Searching latest news about {query}"