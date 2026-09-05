import re

from tools.app_tools import (
    open_notepad,
    open_calculator,
    open_explorer,
    open_command_prompt,
    open_powershell,
    open_vscode,
    open_chrome,
    open_application,
    close_app,
    lock_pc,
    minimize_all_windows,
    show_desktop,
)



class AppIntents:

    def open_app(self, command):

        patterns = [
            r"^open (.+)$",
            r"^launch (.+)$",
            r"^start (.+)$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                command,
                re.IGNORECASE
            )

            if not match:
                continue

            app_name = match.group(1).strip()

            if not app_name:
                return "Please provide an application name."

            # Prevent browser/file commands from being treated as apps
            blocked = [
                "website",
                "google",
                "youtube",
                "github",
                "file",
                "folder",
                "path",
            ]

            if app_name.lower() in blocked:
                return None

            return open_application(app_name)

        return None
    def open_application(self, command):

        patterns = [
            r"open (.+)",
            r"launch (.+)",
            r"start (.+)",
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                command,
                re.IGNORECASE
            )

            if not match:
                continue

            app = match.group(1).strip().lower()

            if app in ["notepad", "note pad"]:
                return open_notepad()

            if app in ["calculator", "calc"]:
                return open_calculator()

            if app in ["file explorer", "explorer"]:
                return open_explorer()

            if app in ["command prompt", "cmd"]:
                return open_command_prompt()

            if app in ["powershell", "power shell"]:
                return open_powershell()

            if app in ["vscode", "vs code", "visual studio code"]:
                return open_vscode()

            if app in ["chrome", "google chrome"]:
                return open_chrome()

        return None

    def close_application(self, command):

        patterns = [
            r"^close (.+)$",
            r"^exit (.+)$",
            r"^quit (.+)$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                command,
                re.IGNORECASE
            )

            if match:

                app_name = match.group(1).strip()

                if not app_name:
                    return "Please provide an application name."

                return close_app(app_name)

        return None

    def system_actions(self, command):

        if command in [
            "lock pc",
            "lock computer",
            "lock my pc",
        ]:
            return lock_pc()

        if command in [
            "minimize all windows",
            "minimize all",
        ]:
            return minimize_all_windows()

        if command in [
            "show desktop",
            "show my desktop",
        ]:
            return show_desktop()

        return None

    def execute(self, command):

        # System actions
        if command in [
            "lock pc",
            "lock computer",
            "lock my pc",
        ]:
            return lock_pc()

        if command in [
            "minimize all",
            "minimize all windows",
        ]:
            return minimize_all_windows()

        if command in [
            "show desktop",
            "show my desktop",
        ]:
            return show_desktop()

        # Close application
        result = self.close_application(command)

        if result:
            return result

        # Open application
        result = self.open_app(command)

        if result:
            return result

        return None