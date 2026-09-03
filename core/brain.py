
import time

from google import genai
from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_PROMPT


class JarvisBrain:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

    def ask(self, user_message):

        max_retries = 3

        for attempt in range(max_retries):

            try:

                response = self.chat.send_message(
                    message=user_message
                )

                return response.text.strip()

            except Exception as e:

                error_message = str(e)

                # Gemini server temporarily overloaded
                if "503" in error_message or "UNAVAILABLE" in error_message:

                    if attempt < max_retries - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"⚠️ Gemini busy. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                        continue

                raise e

