import json
import os
import threading
import time
import uuid
from datetime import datetime, timedelta


class ReminderManager:

    def __init__(self, speaker=None):
        self.speaker = speaker
        self.memory_dir = "memory"
        self.reminder_file = os.path.join(
            self.memory_dir,
            "reminders.json"
        )

        os.makedirs(self.memory_dir, exist_ok=True)

        if not os.path.exists(self.reminder_file):
            self._save([])

        self.reminders = self._load()

        # Background reminder checker
        self.running = True

        self.thread = threading.Thread(
            target=self._check_reminders,
            daemon=True
        )

        self.thread.start()

    def _load(self):
        try:
            with open(
                self.reminder_file,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data):
        with open(
            self.reminder_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def add_reminder(self, text, minutes):
        try:
            minutes = int(minutes)

            if minutes <= 0:
                return "Please provide a valid reminder time."

            remind_at = datetime.now() + timedelta(
                minutes=minutes
            )

            reminder = {
                "id": str(uuid.uuid4())[:8],
                "text": text.strip(),
                "remind_at": remind_at.isoformat(),
                "completed": False
            }

            self.reminders = self._load()
            self.reminders.append(reminder)
            self._save(self.reminders)

            return (
                f"Reminder set for {minutes} minutes from now. "
                f"I will remind you to {text.strip()}."
            )

        except ValueError:
            return "Please provide a valid number of minutes."

    def list_reminders(self):
        self.reminders = self._load()

        pending = [
            reminder
            for reminder in self.reminders
            if not reminder.get("completed", False)
        ]

        if not pending:
            return "You have no pending reminders."

        result = ["Your pending reminders are:"]

        for reminder in pending:
            remind_at = datetime.fromisoformat(
                reminder["remind_at"]
            )

            result.append(
                f"- {reminder['id']}: "
                f"{reminder['text']} at "
                f"{remind_at.strftime('%Y-%m-%d %I:%M %p')}"
            )

        return "\n".join(result)

    def cancel_reminder(self, reminder_id):
        self.reminders = self._load()

        found = False

        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                reminder["completed"] = True
                found = True
                break

        if not found:
            return "I could not find that reminder."

        self._save(self.reminders)

        return "Reminder cancelled successfully."

    def _check_reminders(self):

        while self.running:

            try:

                # Always load the latest reminders
                self.reminders = self._load()

                now = datetime.now()

                for reminder in self.reminders:

                    # Skip completed reminders
                    if reminder.get("completed", False):
                        continue

                    reminder_time = datetime.fromisoformat(
                        reminder["remind_at"]
                    )

                    if now >= reminder_time:

                        message = f"Reminder: {reminder['text']}"

                        print(f"\n⏰ {message}")

                        # Mark completed before speaking
                        reminder["completed"] = True

                        # Correct method name
                        self._save(self.reminders)

                        # Speak reminder
                        if self.speaker:

                            try:

                                self.speaker.speak(message)

                            except Exception as e:

                                print(
                                    f"🔊 Reminder TTS Error: {e}"
                                )

                        else:

                            print(
                                "⚠️ Reminder speaker is not connected."
                            )

            except Exception as e:

                print(f"⏰ Reminder Error: {e}")

            time.sleep(2)

            while True:

                now = datetime.now()

                for reminder in self.reminders:

                    if reminder["completed"]:
                        continue

                    reminder_time = datetime.fromisoformat(
                        reminder["remind_at"]
                    )

                    if now >= reminder_time:

                        message = f"Reminder: {reminder['text']}"

                        print(f"\n⏰ {message}")

                        # Mark completed
                        reminder["completed"] = True

                        # Save updated reminders
                        self._save(self.reminders)

                        # Speak reminder
                        if self.speaker:

                            try:

                                self.speaker.speak(message)

                            except Exception as e:

                                print(f"🔊 Reminder TTS Error: {e}")

                        else:

                            print("⚠️ Reminder speaker is not connected.")

                time.sleep(2)