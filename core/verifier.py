import os


class TaskVerifier:

    def verify(self, step, result):

        if not step:
            return False

        action = str(
            step.get("action", "")
        ).lower().strip()

        parameters = step.get(
            "parameters",
            {}
        )

        # --------------------------------------------------
        # CREATE FOLDER
        # --------------------------------------------------

        if action == "create_folder":

            folder_name = (
                parameters.get("folder_name")
                or parameters.get("name")
                or parameters.get("folder")
            )

            location = (
                parameters.get("resolved_location")
                or parameters.get("location")
                or parameters.get("path")
            )

            if not folder_name or not location:
                print("❌ Verifier: folder name/location missing.")
                return False

            folder_path = os.path.normpath(
                os.path.join(
                    str(location),
                    str(folder_name)
                )
            )

            print(
                f"🔍 Verifying folder: {folder_path}"
            )

            if os.path.isdir(folder_path):

                print(
                    f"✅ Folder verified: {folder_path}"
                )

                return True

            print(
                f"❌ Folder does not exist: {folder_path}"
            )

            return False

        # --------------------------------------------------
        # CREATE FILE
        # --------------------------------------------------

        if action == "create_file":

            file_name = (
                parameters.get("file_name")
                or parameters.get("filename")
                or parameters.get("name")
                or parameters.get("file")
            )

            location = (
                parameters.get("resolved_location")
                or parameters.get("location")
                or parameters.get("path")
            )

            if not file_name or not location:
                print("❌ Verifier: file name/location missing.")
                return False

            file_path = os.path.normpath(
                os.path.join(
                    str(location),
                    str(file_name)
                )
            )

            print(
                f"🔍 Verifying file: {file_path}"
            )

            if os.path.isfile(file_path):

                print(
                    f"✅ File verified: {file_path}"
                )

                return True

            print(
                f"❌ File does not exist: {file_path}"
            )

            return False

        # --------------------------------------------------
        # OTHER ACTIONS
        # --------------------------------------------------

        if result is None:
            print(
                f"⚠️ No return value from action: {action}"
            )

        # For actions that don't have filesystem
        # verification yet, consider execution successful
        # unless an explicit failure message exists.

        if isinstance(result, str):

            failure_words = [
                "failed",
                "failure",
                "error",
                "could not",
                "couldn't",
                "unable",
                "not found",
                "does not exist",
            ]

            result_lower = result.lower()

            for word in failure_words:

                if word in result_lower:
                    print(
                        f"❌ Verifier detected failure: {word}"
                    )
                    return False

        return True

    # ------------------------------------------------------
    # VERIFY COMPLETE PLAN
    # ------------------------------------------------------

    def verify_plan(self, execution_result):

        if not execution_result:
            return False

        if not execution_result.get(
            "success",
            False
        ):
            return False

        results = execution_result.get(
            "results",
            []
        )

        if not results:
            return False

        return True