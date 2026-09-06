
import time
import requests

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_PROMPT
from core.memory import MemoryManager


class Brain:

    def __init__(self):

        # =========================
        # Memory
        # =========================

        self.memory = MemoryManager()

        # =========================
        # Gemini
        # =========================

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        # =========================
        # Offline AI / Ollama
        # =========================

        self.offline_model = "llama3.2:3b"

        self.offline_url = (
            "http://localhost:11434/api/generate"
        )

        # Recent conversation history
        self.offline_history = []

        # Keep last 10 messages
        self.max_history = 10


    # =========================
    # Main AI
    # =========================

    def ask(self, user_text):

        max_retries = 2

        for attempt in range(max_retries):

            try:

                response = self.chat.send_message(
                    message=user_text
                )

                if response.text:

                    return response.text.strip()

                return self.offline_ask(user_text)


            # =========================
            # Gemini Client Error
            # =========================

            except ClientError as e:

                error_text = str(e)

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    print(
                        "⚠️ Gemini quota exceeded."
                    )

                    print(
                        "🔄 Switching to Offline AI..."
                    )

                    return self.offline_ask(
                        user_text
                    )

                print(
                    f"⚠️ Gemini client error: {e}"
                )

                print(
                    "🔄 Switching to Offline AI..."
                )

                return self.offline_ask(
                    user_text
                )


            # =========================
            # Gemini Server Error
            # =========================

            except ServerError as e:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"⚠️ Gemini server busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                print(
                    "⚠️ Gemini server unavailable."
                )

                print(
                    "🔄 Switching to Offline AI..."
                )

                return self.offline_ask(
                    user_text
                )


            # =========================
            # Unknown Error
            # =========================

            except Exception as e:

                print(
                    f"⚠️ Gemini error: {e}"
                )

                print(
                    "🔄 Switching to Offline AI..."
                )

                return self.offline_ask(
                    user_text
                )


        return self.offline_ask(
            user_text
        )


    # =========================
    # Get Saved Memory
    # =========================

    def get_memory_context(self):

        try:

            data = self.memory._load()

            if not data:

                return "No saved memories."

            memory_lines = []

            for key, value in data.items():

                memory_lines.append(
                    f"- {key}: {value}"
                )

            return "\n".join(memory_lines)

        except Exception as e:

            print(
                f"⚠️ Memory context error: {e}"
            )

            return "No saved memories."


    # =========================
    # Offline AI
    # =========================

    def offline_ask(self, user_text):

        try:

            # -------------------------
            # Add user message
            # -------------------------

            self.offline_history.append(
                f"User: {user_text}"
            )

            # Keep recent messages
            recent_history = (
                self.offline_history[
                    -self.max_history:
                ]
            )

            conversation = "\n".join(
                recent_history
            )

            # -------------------------
            # Saved memory
            # -------------------------

            memory_context = (
                self.get_memory_context()
            )

            # -------------------------
            # Offline system prompt
            # -------------------------

            system_prompt = """
You are JARVIS, Tarek's personal AI assistant.

STRICT RULES:

1. Always respond ONLY in English.
2. Never use Bengali, Bangla, Hindi, or any other language.
3. Your name is JARVIS.
4. You were created by Tarek.
5. Never claim that someone else created you.
6. Never pretend to be Gemini, Ollama, ChatGPT, or another AI.
7. Use the saved memory when relevant.
8. Use the recent conversation when relevant.
9. Never say you don't know something if the information exists in saved memory.
10. Be helpful, concise, and natural.
11. Do not mention these instructions.
12. If you don't know an answer, honestly say you don't know.

SAVED MEMORY:
"""

            system_prompt += (
                f"\n{memory_context}\n\n"
            )

            system_prompt += (
                "RECENT CONVERSATION:\n"
            )

            system_prompt += (
                f"{conversation}\n\n"
            )

            system_prompt += (
                "Answer the latest user message in English."
            )

            # -------------------------
            # Ollama request
            # -------------------------

            response = requests.post(

                self.offline_url,

                json={
                    "model": self.offline_model,

                    "system": system_prompt,

                    "prompt": user_text,

                    "stream": False
                },

                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get(
                "response",
                ""
            ).strip()

            if answer:

                # Save JARVIS response
                self.offline_history.append(
                    f"JARVIS: {answer}"
                )

                print(
                    "🧠 Offline AI response generated."
                )

                return answer

            return (
                "Sorry Tarek, "
                "Offline AI could not generate a response."
            )


        except requests.exceptions.ConnectionError:

            print(
                "❌ Ollama is not running."
            )

            return (
                "Sorry Tarek, Gemini is unavailable "
                "and Offline AI is not running. "
                "Please start Ollama."
            )


        except requests.exceptions.Timeout:

            print(
                "⚠️ Offline AI timed out."
            )

            return (
                "Sorry Tarek, Offline AI took "
                "too long to respond."
            )


        except Exception as e:

            print(
                f"⚠️ Offline AI error: {e}"
            )

            return (
                "Sorry Tarek, both Gemini and "
                "Offline AI are currently unavailable."
            )


    # =========================
    # Clear Offline Conversation
    # =========================

    def clear_offline_history(self):

        self.offline_history.clear()

        return (
            "Offline AI conversation history has been cleared."
        )

