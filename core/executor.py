import os
import re


class TaskExecutor:

    def __init__(self, intent_manager):

        self.intent_manager = intent_manager

        # Stores information produced by previous steps.
        # This allows later steps to use earlier results.
        self.context = {}

    # ============================================================
    # EXECUTE PLAN
    # ============================================================

    def execute_plan(self, plan):

        if not isinstance(plan, dict):

            return {
                "success": False,
                "results": [],
                "message": "Invalid task plan."
            }

        steps = plan.get("steps", [])

        if not isinstance(steps, list) or not steps:

            return {
                "success": False,
                "results": [],
                "message": "No executable steps found."
            }

        # Reset context for every new autonomous task
        self.context = {}

        results = []

        for step in steps:

            result = self.execute_step(step)

            results.append({
                "step": step.get("step"),
                "action": step.get("action"),
                "result": result
            })

            if not self._is_success(result):

                return {
                    "success": False,
                    "results": results,
                    "message": (
                        f"Step {step.get('step')} failed."
                    )
                }

        return {
            "success": True,
            "results": results,
            "message": "All steps executed successfully."
        }

    # ============================================================
    # EXECUTE SINGLE STEP
    # ============================================================

    def execute_step(self, step):

        if not isinstance(step, dict):

            return "Invalid task step."

        action = step.get("action")

        parameters = step.get(
            "parameters",
            {}
        )

        description = step.get(
            "description",
            ""
        )

        if not action:

            return "Step action is missing."

        action = str(
            action
        ).strip().lower()

        if not isinstance(parameters, dict):

            parameters = {}

        print(
            f"\n⚙️ Executing: {description}"
        )

        print(
            f"🔧 Action: {action}"
        )

        print(
            f"📦 Parameters: {parameters}"
        )

        try:

            # ====================================================
            # Resolve parameters
            # ====================================================

            parameters = self._prepare_parameters(
                action,
                parameters
            )

            print(
                f"📍 Resolved Parameters: {parameters}"
            )

            # ====================================================
            # Direct structured execution
            # ====================================================

            ai_result = {
                "intent": self._get_intent(action),
                "action": action,
                "parameters": parameters
            }

            print(
                f"🚀 Direct Tool Execution: {ai_result}"
            )

            result = self.intent_manager.execute_ai_intent(
                ai_result
            )

            if result is None:

                return (
                    f"JARVIS could not execute: "
                    f"{description}"
                )

            # ====================================================
            # Save useful execution context
            # ====================================================

            self._store_context(
                action,
                parameters,
                result
            )

            return result

        except Exception as e:

            return (
                f"Execution error: {e}"
            )

    # ============================================================
    # PREPARE PARAMETERS
    # ============================================================

    def _prepare_parameters(
        self,
        action,
        parameters
    ):

        parameters = dict(parameters)

        # --------------------------------------------------------
        # CREATE FOLDER
        # --------------------------------------------------------

        if action == "create_folder":

            name = (
                parameters.get("name")
                or parameters.get("folder_name")
            )

            location = (
                parameters.get("location")
                or parameters.get("path")
                or parameters.get("parent")
                or parameters.get("directory")
            )

            if name:

                parameters["name"] = str(
                    name
                ).strip()

            if location:

                parameters["location"] = (
                    self._resolve_autonomous_location(
                        location
                    )
                )

            return parameters

        # --------------------------------------------------------
        # CREATE FILE
        # --------------------------------------------------------

        if action == "create_file":

            name = (
                parameters.get("name")
                or parameters.get("file_name")
                or parameters.get("filename")
                or parameters.get("file")
            )

            location = (
                parameters.get("location")
                or parameters.get("path")
                or parameters.get("directory")
                or parameters.get("folder")
            )

            if name:

                parameters["name"] = str(
                    name
                ).strip()

            if location:

                parameters["location"] = (
                    self._resolve_autonomous_location(
                        location
                    )
                )

            # Default content
            if "content" not in parameters:

                parameters["content"] = ""

            return parameters

        # --------------------------------------------------------
        # OPEN FILE / FOLDER
        # --------------------------------------------------------

        if action in [
            "open_file",
            "open_folder",
            "open_directory",
            "open_path",
        ]:

            path = (
                parameters.get("path")
                or parameters.get("file")
                or parameters.get("folder")
                or parameters.get("directory")
                or parameters.get("name")
            )

            if path:

                parameters["path"] = (
                    self._resolve_autonomous_location(
                        path
                    )
                )

            return parameters

        # --------------------------------------------------------
        # SEARCH FILE
        # --------------------------------------------------------

        if action == "search_file":

            query = (
                parameters.get("query")
                or parameters.get("name")
                or parameters.get("filename")
                or parameters.get("file")
            )

            if query:

                parameters["query"] = str(
                    query
                ).strip()

            return parameters

        # --------------------------------------------------------
        # RENAME
        # --------------------------------------------------------

        if action in [
            "rename_file",
            "rename_folder",
            "rename_item",
            "rename",
        ]:

            old_name = (
                parameters.get("old_name")
                or parameters.get("old")
                or parameters.get("source")
            )

            new_name = (
                parameters.get("new_name")
                or parameters.get("new")
                or parameters.get("destination")
            )

            if old_name:
                parameters["old_name"] = old_name

            if new_name:
                parameters["new_name"] = new_name

            return parameters

        # --------------------------------------------------------
        # APPLICATION
        # --------------------------------------------------------

        if action in [
            "open_app",
            "open_application",
            "close_app",
            "close_application",
        ]:

            app = (
                parameters.get("app")
                or parameters.get("application")
                or parameters.get("name")
            )

            if app:

                parameters["app"] = str(
                    app
                ).strip()

            return parameters

        return parameters

    # ============================================================
    # AUTONOMOUS LOCATION RESOLVER
    # ============================================================

    def _resolve_autonomous_location(
        self,
        location
    ):

        if not location:

            return None

        location = str(
            location
        ).strip()

        if not location:

            return None

        # --------------------------------------------------------
        # Already an absolute path
        # --------------------------------------------------------

        if (
            ":" in location
            or location.startswith("\\")
            or location.startswith("/")
        ):

            return os.path.normpath(
                location
            )

        # --------------------------------------------------------
        # Step 1 context
        #
        # If previous step created a folder, use it.
        # --------------------------------------------------------

        if location.lower() in [
            "newly created folder",
            "new folder",
            "created folder",
            "that folder",
            "the folder",
        ]:

            created_folder = self.context.get(
                "last_created_folder"
            )

            if created_folder:

                return created_folder

        # --------------------------------------------------------
        # Composite locations
        #
        # Example:
        # project folder/V3Test
        # project folder\V3Test
        # --------------------------------------------------------

        normalized = location.replace(
            "\\",
            "/"
        )

        parts = [
            part.strip()
            for part in normalized.split("/")
            if part.strip()
        ]

        if len(parts) > 1:

            base_name = parts[0]

            remainder = parts[1:]

            base_path = (
                self._safe_resolve_location(
                    base_name
                )
            )

            if base_path:

                full_path = base_path

                for part in remainder:

                    full_path = os.path.join(
                        full_path,
                        part
                    )

                return os.path.normpath(
                    full_path
                )

        # --------------------------------------------------------
        # Check whether this matches previous created folder
        # --------------------------------------------------------

        last_folder = self.context.get(
            "last_created_folder"
        )

        if last_folder:

            if os.path.basename(
                last_folder
            ).lower() == location.lower():

                return last_folder

        # --------------------------------------------------------
        # Normal JARVIS resolver
        # --------------------------------------------------------

        return self._safe_resolve_location(
            location
        )

    # ============================================================
    # SAFE LOCATION RESOLUTION
    # ============================================================

    def _safe_resolve_location(
        self,
        location
    ):

        try:

            resolved = (
                self.intent_manager.resolve_location(
                    location
                )
            )

            if resolved:

                return os.path.normpath(
                    resolved
                )

        except Exception:

            pass

        return location

    # ============================================================
    # ACTION → INTENT
    # ============================================================

    def _get_intent(
        self,
        action
    ):

        action = str(
            action
        ).strip().lower()

        # File actions
        if action in [
            "create_folder",
            "create_file",
            "open_file",
            "open_folder",
            "open_directory",
            "open_path",
            "search_file",
            "rename_file",
            "rename_folder",
            "rename_item",
            "rename",
            "write_file",
            "append_file",
            "read_file",
            "file_info",
            "delete_file",
            "delete_folder",
            "delete_item",
            "move_file",
            "move_folder",
            "move_item",
            "move",
        ]:

            return "files"

        # Applications
        if action in [
            "open_app",
            "open_application",
        ]:

            return "open_application"

        if action in [
            "close_app",
            "close_application",
        ]:

            return "close_application"

        if action in [
            "minimize_app",
            "minimize_application",
        ]:

            return "minimize_application"

        if action in [
            "maximize_app",
            "maximize_application",
        ]:

            return "maximize_application"

        # Browser
        if action == "google_search":

            return "google_search"

        if action == "youtube_search":

            return "youtube_search"

        if action == "open_website":

            return "open_website"

        # System
        if action == "get_time":

            return "get_time"

        if action == "get_date":

            return "get_date"

        if action == "system_status":

            return "system_status"

        if action == "battery":

            return "battery"

        if action == "cpu_usage":

            return "cpu_usage"

        if action == "ram_usage":

            return "ram_usage"

        if action == "disk_space":

            return "disk_space"

        # Volume
        if action in [
            "set_volume",
            "increase_volume",
            "decrease_volume",
            "mute_volume",
            "unmute_volume",
        ]:

            return action

        # Clipboard
        if action in [
            "read_clipboard",
            "clear_clipboard",
            "copy_to_clipboard",
        ]:

            return action

        # Screenshot
        if action == "screenshot":

            return "screenshot"

        # Fallback
        return action

    # ============================================================
    # STORE EXECUTION CONTEXT
    # ============================================================

    def _store_context(
        self,
        action,
        parameters,
        result
    ):

        # Save the last result
        self.context["last_result"] = result

        # --------------------------------------------------------
        # Created folder
        # --------------------------------------------------------

        if action == "create_folder":

            location = parameters.get(
                "location"
            )

            name = parameters.get(
                "name"
            )

            if location and name:

                folder_path = os.path.normpath(
                    os.path.join(
                        str(location),
                        str(name)
                    )
                )

                if os.path.isdir(
                    folder_path
                ):

                    self.context[
                        "last_created_folder"
                    ] = folder_path

                    print(
                        f"📁 Created folder: "
                        f"{folder_path}"
                    )

        # --------------------------------------------------------
        # Created file
        # --------------------------------------------------------

        if action == "create_file":

            location = parameters.get(
                "location"
            )

            name = parameters.get(
                "name"
            )

            if location and name:

                file_path = os.path.normpath(
                    os.path.join(
                        str(location),
                        str(name)
                    )
                )

                if os.path.isfile(
                    file_path
                ):

                    self.context[
                        "last_created_file"
                    ] = file_path

                    print(
                        f"📄 Created file: "
                        f"{file_path}"
                    )

    # ============================================================
    # RESULT CHECK
    # ============================================================

    def _is_success(
        self,
        result
    ):

        if result is None:

            return False

        if isinstance(
            result,
            bool
        ):

            return result

        text = str(
            result
        ).lower()

        failure_words = [
            "failed",
            "failure",
            "error",
            "could not",
            "couldn't",
            "unable",
            "not found",
            "does not exist",
            "no such file",
        ]

        for word in failure_words:

            if word in text:

                return False

        return True