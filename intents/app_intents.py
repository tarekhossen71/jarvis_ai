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
    minimize_application,
    maximize_application,
    switch_to_application,
    get_active_window,
    switch_to_next_window,
    switch_to_previous_window,
    get_open_windows,
    restore_all_windows,
    move_application,
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


    # =========================
    # Window Control
    # =========================

    def minimize_application(self, command):

        match = re.fullmatch(
            r"minimize (.+)",
            command,
            re.IGNORECASE
        )

        if not match:
            return None

        app_name = match.group(1).strip()

        if not app_name:
            return "Please provide an application name."

        return minimize_application(app_name)


    def maximize_application(self, command):

        match = re.fullmatch(
            r"maximize (.+)",
            command,
            re.IGNORECASE
        )

        if not match:
            return None

        app_name = match.group(1).strip()

        if not app_name:
            return "Please provide an application name."

        return maximize_application(app_name)


    def switch_to_application(self, command):

        match = re.fullmatch(
            r"(?:switch to|focus) (.+)",
            command,
            re.IGNORECASE
        )

        if not match:
            return None

        app_name = match.group(1).strip()

        if not app_name:
            return "Please provide an application name."

        return switch_to_application(app_name)

        # =========================
    
    
    # Active Window
    # =========================

    def active_window(self, command):

        if command in [
            "what window is active",
            "which window is active",
            "active window",
            "current window",
            "what app is active",
            "which app is active",
            "what am i working on",
        ]:
            return get_active_window()

        return None

    
    # =========================
    # Window Navigation
    # =========================

    def window_navigation(self, command):

        if command in [
            "switch to next window",
            "next window",
            "switch next window",
            "next window please",
        ]:
            return switch_to_next_window()

        if command in [
            "switch to previous window",
            "previous window",
            "switch previous window",
            "previous window please",
        ]:
            return switch_to_previous_window()

        return None

    def open_windows(self, command):
        if command in [
            "what windows are open",
            "which windows are open",
            "show open windows",
            "list open windows",
            "open windows",
            "show windows",
            "what apps are open",
            "which apps are open",
        ]:
            return get_open_windows()

        return None

    def restore_all(self, command):
        if command in [
            "restore all windows",
            "restore all",
            "restore windows",
            "show all windows",
        ]:
            return restore_all_windows()

        return None

    def move_app(self, command):
        patterns = [
            r"^move (.+) to (\d+),\s*(\d+)$",
            r"^move (.+) to position (\d+),\s*(\d+)$",
        ]

        for pattern in patterns:
            match = re.fullmatch(pattern, command, re.IGNORECASE)

            if match:
                app_name = match.group(1).strip()
                x = int(match.group(2))
                y = int(match.group(3))

                return move_application(app_name, x, y)

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

        # Window Navigation
        result = self.window_navigation(command)
        if result:
            return result
        
        # Open windows
        result = self.open_windows(command)
        if result:
            return result

        
        # Close application
        result = self.close_application(command)

        if result:
            return result

        # Open application
        result = self.open_app(command)
        if result:
            return result

        # Active Window
        result = self.active_window(command)
        if result:
            return result
    
        # Window Control
        result = self.minimize_application(command)
        if result:
            return result
        

        result = self.maximize_application(command)
        if result:
            return result

        # Restore all windows
        result = self.restore_all(command)
        if result:
            return result

        result = self.switch_to_application(command)
        if result:
            return result
        # Move application
        result = self.move_app(command)
        if result:
            return result


        
        return None