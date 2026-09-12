import re


class CommunicationIntents:

    def __init__(self, tools, confirmation):
        self.tools = tools
        self.confirmation = confirmation
        # Email conversation state
        self.email_state = None
        self.email_data = {
            "to": "",
            "subject": "",
            "body": "",
        }

        # WhatsApp conversation state
        self.whatsapp_state = None
        self.whatsapp_data = {
            "phone": "",
            "message": "",
        }

    def normalize(self, text):
        return text.lower().strip()

    # =========================
    # WhatsApp
    # =========================

    def open_whatsapp(self, command):
        text = self.normalize(command)

        commands = [
            "open whatsapp",
            "start whatsapp",
            "launch whatsapp",
            "open whatsapp web",
            "start whatsapp web",
        ]

        if text in commands:
            return self.tools.open_whatsapp()

        return None

    # =========================
    # Email
    # =========================

    def open_email(self, command):
        text = self.normalize(command)

        commands = [
            "open email",
            "open gmail",
            "start email",
            "start gmail",
            "launch email",
            "launch gmail",
        ]

        if text in commands:
            return self.tools.open_email()

        return None

    # =========================
    # Start Email Compose
    # =========================

    def compose_email(self, command):
        text = self.normalize(command)

        patterns = [
            r"email (.+)",
            r"send email to (.+)",
            r"compose email to (.+)",
            r"write email to (.+)",
            r"send an email to (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                recipient = match.group(1).strip()

                if not recipient:
                    return "Please provide the email address."

                # Basic email validation
                if "@" not in recipient:
                    return "Please provide a valid email address."

                # Start conversation
                self.email_data = {
                    "to": recipient,
                    "subject": "",
                    "body": "",
                }

                self.email_state = "subject"

                return (
                    f"Email recipient set to {recipient}. "
                    "What is the subject?"
                )

        return None

    # =========================
    # Email Conversation
    # =========================

    def email_conversation(self, command):

        if not self.email_state:
            return None

        text = command.strip()

        if not text:
            return "Please provide the required information."

        # -------------------------
        # Subject
        # -------------------------

        if self.email_state == "subject":

            self.email_data["subject"] = text

            self.email_state = "body"

            return "What should I write in the email?"

        # -------------------------
        # Body
        # -------------------------

        if self.email_state == "body":

            self.email_data["body"] = text

            to = self.email_data["to"]
            subject = self.email_data["subject"]
            body = self.email_data["body"]

            # Reset state before opening browser
            self.email_state = None

            self.email_data = {
                "to": "",
                "subject": "",
                "body": "",
            }

            return self.tools.compose_email(
                to=to,
                subject=subject,
                body=body
            )

        return None

    def whatsapp_message(self, command):
        text = self.normalize(command)

        patterns = [
            r"send whatsapp message to (.+)",
            r"send whatsapp to (.+)",
            r"whatsapp message to (.+)",
            r"message on whatsapp to (.+)",
            r"message whatsapp to (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                phone = match.group(1).strip()

                # Extract only phone-like characters
                phone_clean = re.sub(
                    r"[^\d+]",
                    "",
                    phone
                )

                if not phone_clean:
                    return "Please provide a valid phone number."

                self.whatsapp_data = {
                    "phone": phone_clean,
                    "message": "",
                }

                self.whatsapp_state = "message"

                return "What message should I send?"

        return None

    def whatsapp_conversation(self, command):

        if not self.whatsapp_state:
            return None

        text = command.strip()

        if not text:
            return "Please provide the message."

        if self.whatsapp_state == "message":

            phone = self.whatsapp_data["phone"]
            message = text

            # Message + phone temporary save
            self.whatsapp_data["message"] = message

            # Reset conversation state
            self.whatsapp_state = None

            # Confirmation-er age WhatsApp open hobe na
            return self.confirmation.ask(
                f"send WhatsApp message to {phone}",
                lambda: self.send_confirmed_whatsapp()
            )

        return None

    def send_confirmed_whatsapp(self):
        phone = self.whatsapp_data["phone"]
        message = self.whatsapp_data["message"]

        # YES bolar por WhatsApp open + message type
        result = self.tools.open_whatsapp_chat(
            phone,
            message
        )

        # WhatsApp open na hole send korbe na
        if result.startswith("Failed") or result.startswith("Please"):
            self.whatsapp_data = {
                "phone": "",
                "message": "",
            }
            return result

        # Message box-e message ready howar por send
        result = self.tools.send_whatsapp_message()

        # Clear saved data
        self.whatsapp_data = {
            "phone": "",
            "message": "",
        }

        return result

    # =========================
    # Main Communication
    # =========================

    def execute(self, command):

        # =========================
        # Email Conversation
        # =========================

        if self.email_state:

            result = self.email_conversation(command)

            if result is not None:
                return result

        # =========================
        # WhatsApp Conversation
        # =========================

        if self.whatsapp_state:

            result = self.whatsapp_conversation(command)

            if result is not None:
                return result

        # =========================
        # WhatsApp
        # =========================

        result = self.open_whatsapp(command)

        if result is not None:
            return result

        # =========================
        # Email
        # =========================

        result = self.open_email(command)

        if result is not None:
            return result

        result = self.compose_email(command)

        if result is not None:
            return result

        # =========================
        # WhatsApp Message
        # =========================

        result = self.whatsapp_message(command)

        if result is not None:
            return result

        return None