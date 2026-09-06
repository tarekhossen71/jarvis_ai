import time

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_PROMPT


class Brain:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

    def ask(self, user_text):

        max_retries = 2

        for attempt in range(max_retries):

            try:

                response = self.chat.send_message(
                    message=user_text
                )

                if response.text:

                    return response.text.strip()

                return "Sorry Tarek, I could not generate a response."

            except ClientError as e:

                error_text = str(e)

                # Quota exceeded
                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                    print("⚠️ Gemini quota exceeded.")

                    return (
                        "Sorry Tarek, Gemini API quota is currently exhausted. "
                        "Please try again later."
                    )

                # Other client errors
                print(f"⚠️ Gemini client error: {e}")

                return (
                    "Sorry Tarek, I could not connect to Gemini right now."
                )

            except ServerError as e:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"⚠️ Gemini server busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return (
                    "Gemini server is currently busy. "
                    "Please try again later."
                )

            except Exception as e:

                print(f"⚠️ Gemini error: {e}")

                return (
                    "Sorry Tarek, something went wrong. "
                    "But JARVIS is still running."
                )

        return "Sorry Tarek, I could not get a response."