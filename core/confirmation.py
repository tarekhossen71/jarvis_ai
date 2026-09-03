class ConfirmationManager:

    def __init__(self):
        self.pending_action = None

    def ask(self, action, callback):
        self.pending_action = {
            "action": action,
            "callback": callback
        }

        return f"Are you sure you want me to {action}? Please say yes or no."

    def confirm(self):
        if not self.pending_action:
            return "There is no pending action."

        callback = self.pending_action["callback"]

        self.pending_action = None

        return callback()

    def cancel(self):
        self.pending_action = None

        return "Okay, I cancelled the action."

    def has_pending(self):
        return self.pending_action is not None