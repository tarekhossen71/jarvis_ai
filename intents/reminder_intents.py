import re


class ReminderIntents:
    def __init__(self, reminder):
        self.reminder = reminder

    def normalize(self, text):
        return text.lower().strip()

    def create_reminder(self, command):
        """
        Examples:
        remind me to drink water in 10 minutes
        set a reminder to call mom after 5 minutes
        """

        text = self.normalize(command)

        if not any(keyword in text for keyword in [
            "remind me",
            "set a reminder",
            "create a reminder",
            "add a reminder"
        ]):
            return None

        # Extract reminder message
        message_match = re.search(
            r"(?:remind me to|set a reminder to|create a reminder to|add a reminder to)\s+(.+?)\s+(?:in|after)\s+\d+\s*(?:minute|minutes|min|hour|hours|hr|hrs)",
            text
        )

        if not message_match:
            return None

        message = message_match.group(1).strip()

        # Extract time
        time_match = re.search(
            r"(?:in|after)\s+(\d+)\s*(minute|minutes|min|hour|hours|hr|hrs)",
            text
        )

        if not time_match:
            return None

        amount = int(time_match.group(1))
        unit = time_match.group(2)

        if unit in ["hour", "hours", "hr", "hrs"]:
            minutes = amount * 60
        else:
            minutes = amount

        if minutes <= 0:
            return "Reminder time must be greater than zero."

        return self.reminder.add_reminder(message, minutes)

    def list_reminders(self, command):
        text = self.normalize(command)

        if not any(keyword in text for keyword in [
            "show reminders",
            "list reminders",
            "my reminders",
            "what are my reminders"
        ]):
            return None

        reminders = self.reminder.get_reminders()

        if not reminders:
            return "You don't have any active reminders."

        response = "Your active reminders:\n"

        for index, reminder in enumerate(reminders, start=1):
            response += (
                f"{index}. {reminder['message']} "
                f"({reminder['minutes']} minutes)\n"
            )

        return response.strip()

    def cancel_reminder(self, command):
        text = self.normalize(command)

        if not any(keyword in text for keyword in [
            "cancel reminder",
            "delete reminder",
            "remove reminder"
        ]):
            return None

        return self.reminder.cancel_last_reminder()