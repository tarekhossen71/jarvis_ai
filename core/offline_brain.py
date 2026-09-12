
import requests


class OfflineBrain:

    def __init__(self, model="llama3.2:3b"):

        self.model = model
        self.url = "http://localhost:11434/api/generate"

        # Conversation memory
        self.history = []

        # Maximum number of previous messages
        self.max_history = 10

    def ask(self, prompt):

        try:

            # Add user message
            self.history.append(
                f"User: {prompt}"
            )

            # Keep only recent conversation
            recent_history = self.history[-self.max_history:]

            conversation = "\n".join(
                recent_history
            )

            system_prompt = """
You are JARVIS, Tarek's personal AI assistant.

STRICT RULES:

1. Always respond ONLY in English.
2. Never use Bengali, Bangla, Hindi, or any other language.
3. Your name is JARVIS.
4. You were created by Tarek.
5. Never claim that someone else created you.
6. Never pretend to be Gemini, Ollama, ChatGPT, or another AI.
7. Remember the recent conversation context.
8. Use previous messages when answering follow-up questions.
9. Be helpful, concise, and natural.
10. If you don't know something, honestly say you don't know.
"""

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "system": system_prompt,
                    "prompt": conversation,
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
                self.history.append(
                    f"JARVIS: {answer}"
                )

                print("🧠 Offline AI response generated.")

                return answer

            return (
                "Sorry Tarek, "
                "Offline AI could not generate a response."
            )

        except requests.exceptions.ConnectionError:

            print("❌ Ollama is not running.")

            return (
                "Sorry Tarek, Gemini is unavailable "
                "and Offline AI is not running. "
                "Please start Ollama."
            )

        except requests.exceptions.Timeout:

            print("⚠️ Offline AI timed out.")

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

    def clear_history(self):

        self.history.clear()

        return "Offline AI conversation memory has been cleared."
