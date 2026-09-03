import speech_recognition as sr

from config import INPUT_MODE


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.wake_words = [
            "hey jarvis",
            "hi jarvis",
            "hello jarvis",
            "jarvis",
        ]

    def is_exit_command(self, command):

        command = command.lower().strip()

        return command in [
            "bye",
            "bye jarvis",
            "exit",
            "quit",
            "goodbye",
            "goodbye jarvis",
            "shutdown jarvis",
            "বন্ধ কর",
            "বিদায়",
            "বাই",
        ]

    def is_stop_command(self, command):

        command = command.lower().strip()

        return command in [
            "stop listening",
            "cancel listening",
            "go to sleep",
            "sleep jarvis",
            "শোনা বন্ধ কর",
            "বন্ধ হও",
        ]

    def contains_wake_word(self, text):

        text = text.lower().strip()

        return any(
            text.startswith(wake_word)
            for wake_word in self.wake_words
        )

    def remove_wake_word(self, text):

        text = text.lower().strip()

        for wake_word in self.wake_words:

            if text.startswith(wake_word):

                remaining = text[len(wake_word):].strip()

                if remaining.startswith(","):
                    remaining = remaining[1:].strip()

                return remaining

        return text

    def listen_text(self):

        try:

            return input("👤 You: ").strip()

        except EOFError:

            return "exit"

    def listen_voice(self):

        with self.microphone as source:

            print("🎤 Listening...")

            try:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

                text = self.recognizer.recognize_google(
                    audio,
                    language="en-US"
                )

                print(f"👤 You: {text}")

                return text.lower().strip()

            except sr.WaitTimeoutError:

                print("⏱️ No voice detected.")

                return ""

            except sr.UnknownValueError:

                print("🤖 JARVIS: I could not understand.")

                return ""

            except sr.RequestError:

                print("⚠️ Speech recognition service unavailable.")

                return ""

            except Exception as e:

                print(f"⚠️ Voice error: {e}")

                return ""

    def listen(self):

        if INPUT_MODE.lower() == "text":

            return self.listen_text()

        return self.listen_voice()