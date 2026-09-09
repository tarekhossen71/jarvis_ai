import re


class ReminderIntents:
    def __init__(self, reminder):
        self.reminder = reminder

    def normalize(self, text):
        return text.lower().strip()

    def create_reminder(self, command):
        """
        Relative:
        remind me to drink water in 10 minutes
        set a reminder to call mom after 5 minutes

        Exact time:
        remind me to drink water at 3 pm
        remind me to call mom at 8:30 pm
        """

        from datetime import datetime, timedelta

        text = self.normalize(command)

        reminder_keywords = [
            "remind me",
            "set a reminder",
            "create a reminder",
            "add a reminder"
        ]

        if not any(keyword in text for keyword in reminder_keywords):
            return None

        # =========================================
        # Exact Time Reminder
        # =========================================

        exact_match = re.search(
            r"(?:remind me to|set a reminder to|create a reminder to|add a reminder to)\s+(.+?)\s+at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$",
            text,
            re.IGNORECASE
        )

        if exact_match:

            message = exact_match.group(1).strip()

            hour = int(exact_match.group(2))
            minute = int(exact_match.group(3) or 0)
            meridiem = exact_match.group(4)

            # Validate minute
            if minute > 59:
                return "Please provide a valid minute."

            # 12-hour format
            if meridiem:

                if hour < 1 or hour > 12:
                    return "Please provide a valid hour."

                if meridiem.lower() == "pm" and hour != 12:
                    hour += 12

                elif meridiem.lower() == "am" and hour == 12:
                    hour = 0

            # 24-hour format
            else:

                if hour > 23:
                    return "Please provide a valid hour."

            now = datetime.now()

            remind_at = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            # If today's time has already passed,
            # schedule for tomorrow.
            if remind_at <= now:
                remind_at += timedelta(days=1)

            return self.reminder.add_reminder_at(
                message,
                remind_at
            )

        # =========================================
        # Relative Time Reminder
        # =========================================

        message_match = re.search(
            r"(?:remind me to|set a reminder to|create a reminder to|add a reminder to)\s+(.+?)\s+(?:in|after)\s+\d+\s*(?:minute|minutes|min|hour|hours|hr|hrs)",
            text
        )

        if not message_match:
            return None

        message = message_match.group(1).strip()

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

        return self.reminder.add_reminder(
            message,
            minutes
        )

    def list_reminders(self, command):
        text = self.normalize(command)

        if not any(keyword in text for keyword in [
            "show reminders",
            "list reminders",
            "my reminders",
            "what are my reminders"
        ]):
            return None

        # ReminderManager already returns a formatted string 
        return self.reminder.list_reminders()
    
       

    def cancel_reminder(self, command):

        text = self.normalize(command)

        # =========================================
        # Cancel specific reminder by ID
        # =========================================

        match = re.fullmatch(
            r"(?:cancel|delete|remove) reminder\s+([a-f0-9]{8})",
            text,
            re.IGNORECASE
        )

        if match:
            reminder_id = match.group(1)

            return self.reminder.cancel_reminder(
                reminder_id
            )

        # =========================================
        # Cancel last reminder
        # =========================================

        if text in [
            "cancel reminder",
            "delete reminder",
            "remove reminder",
            "cancel last reminder",
            "delete last reminder",
            "remove last reminder",
        ]:
            return self.reminder.cancel_last_reminder()

        return None

    
    
    
