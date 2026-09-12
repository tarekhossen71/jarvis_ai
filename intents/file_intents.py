import re


class FileIntents:

    def __init__(self, confirmation, tools):
        self.confirmation = confirmation
        self.tools = tools

    def normalize(self, text):
        return text.lower().strip()

    # =========================
    # Create Folder
    # =========================

    def create_folder(self, command):
        text = self.normalize(command)

        patterns = [
            r"^create folder\s+(.+)$",
            r"^make folder\s+(.+)$",
            r"^new folder\s+(.+)$",
        ]

        for pattern in patterns:
            match = re.match(pattern, text, re.IGNORECASE)

            if not match:
                continue

            data = match.group(1).strip()

            # Location provided
            location_match = re.match(
                r"^(.+?)\s+in\s+(.+)$",
                data,
                re.IGNORECASE
            )

            if location_match:
                folder_name = location_match.group(1).strip()
                location = location_match.group(2).strip()

                if not folder_name:
                    return "Please provide a folder name."

                if not location:
                    return "Please provide a location."

                return self.tools.create_folder(
                    folder_name,
                    location
                )

            # No location → user's home directory
            return self.tools.create_folder(data)

        return None

    # =========================
    # Create File
    # =========================

    def create_file(self, command):

        text = self.normalize(command)

        patterns = [
            r"create file (.+)",
            r"make file (.+)",
            r"new file (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if not match:
                continue

            data = match.group(1).strip()

            if not data:
                return "Please provide a file name."

            content = ""
            location = None

            # =========================
            # Extract Content
            # =========================

            content_match = re.search(
                r"\s+with content\s+(.+)",
                data,
                re.IGNORECASE
            )

            if content_match:

                content = content_match.group(1).strip()

                data = data[
                    :content_match.start()
                ].strip()

            # =========================
            # Extract Location
            # =========================

            location_match = re.search(
                r"\s+in\s+(.+)",
                data,
                re.IGNORECASE
            )

            if location_match:

                location = location_match.group(1).strip()

                data = data[
                    :location_match.start()
                ].strip()

            file_name = data.strip()

            if not file_name:
                return "Please provide a file name."

            return self.tools.create_text_file(
                file_name,
                location,
                content
            )

        return None

    # =========================
    # Search Files
    # =========================

    def search_file(self, command):

        text = self.normalize(command)

        patterns = [
            r"search file (.+)",
            r"search files (.+)",
            r"find file (.+)",
            r"find files (.+)",
            r"search for (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                search_name = match.group(1).strip()

                if not search_name:
                    return "Please provide a file or folder name."

                return self.tools.search_files(
                    search_name
                )

        return None

    # =========================
    # File Information
    # =========================

    def file_info(self, command):

        text = self.normalize(command)

        patterns = [
            r"file info (.+)",
            r"file information (.+)",
            r"information about file (.+)",
            r"details of file (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                file_name = match.group(1).strip()

                if not file_name:
                    return "Please provide a file name."

                return self.tools.get_file_info(
                    file_name
                )

        return None

    # =========================
    # Recent Files
    # =========================

    def recent_files(self, command):

        text = self.normalize(command)

        commands = [
            "recent files",
            "show recent files",
            "my recent files",
            "open recent files",
        ]

        if text in commands:

            return self.tools.get_recent_files()

        return None

    # =========================
    # Open Path
    # =========================

    def open_path(self, command):

        text = self.normalize(command)

        prefixes = [
            "open path ",
            "open file path ",
            "open folder path ",
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                path = text[len(prefix):].strip()

                if not path:
                    return "Please provide the path."

                return self.tools.open_path(path)

        return None

    # =========================
    # Rename
    # =========================

    def rename(self, command):

        text = self.normalize(command)

        if not text.startswith("rename "):
            return None

        content = text[7:].strip()

        if " to " not in content:
            return "Please tell me the old name and new name."

        old_name, new_name = content.split(
            " to ",
            1
        )

        old_name = old_name.strip()
        new_name = new_name.strip()

        if not old_name or not new_name:
            return "Please provide both old and new names."

        return self.confirmation.ask(
            f"rename {old_name} to {new_name}",
            lambda: self.tools.rename_item(
                old_name,
                new_name
            )
        )

    # =========================
    # Move
    # =========================

    def move(self, command):

        text = self.normalize(command)

        match = re.match(
            r"move (.+) to (.+)",
            text,
            re.IGNORECASE
        )

        if not match:
            return None

        item_name = match.group(1).strip()
        destination = match.group(2).strip()

        if not item_name or not destination:
            return "Please provide the item and destination."

        return self.confirmation.ask(
            f"move {item_name} to {destination}",
            lambda: self.tools.move_item(
                item_name,
                destination
            )
        )

    # =========================
    # Delete
    # =========================

    def delete(self, command):

        text = self.normalize(command)

        patterns = [
            r"delete file (.+)",
            r"delete folder (.+)",
            r"delete (.+)",
            r"remove file (.+)",
            r"remove folder (.+)",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                item_name = match.group(1).strip()

                if not item_name:
                    return "What should I delete?"

                return self.confirmation.ask(
                    f"delete {item_name}",
                    lambda: self.tools.delete_item(
                        item_name
                    )
                )

        return None

    # =========================
    # Empty Recycle Bin
    # =========================

    def empty_recycle_bin(self, command):

        text = self.normalize(command)

        commands = [
            "empty recycle bin",
            "clear recycle bin",
            "empty the recycle bin",
            "clear the recycle bin",
        ]

        if text in commands:

            return self.confirmation.ask(
                "permanently empty the Recycle Bin",
                self.tools.empty_recycle_bin
            )

        return None

    
    # =========================
    # Open Desktop
    # =========================

    def desktop(self, command):

        text = self.normalize(command)

        commands = [
            "open desktop",
            "desktop kholo",
            "desktop open",
            "ডেস্কটপ খুলো",
            "ডেস্কটপ খুলে দাও",
        ]

        if text in commands:
            return self.tools.open_desktop()

        return None

    # =========================
    # Open Downloads
    # =========================

    def downloads(self, command):

        text = self.normalize(command)

        commands = [
            "open downloads",
            "downloads kholo",
            "downloads open",
            "ডাউনলোড খুলো",
            "ডাউনলোডস খুলো",
        ]

        if text in commands:
            return self.tools.open_downloads()

        return None

    # =========================
    # Open Documents
    # =========================

    def documents(self, command):

        text = self.normalize(command)

        commands = [
            "open documents",
            "documents kholo",
            "documents open",
            "ডকুমেন্টস খুলো",
        ]

        if text in commands:
            return self.tools.open_documents()

        return None

    # =========================
    # Open Pictures
    # =========================

    def pictures(self, command):

        text = self.normalize(command)

        commands = [
            "open pictures",
            "pictures kholo",
            "pictures open",
            "ছবির ফোল্ডার খুলো",
        ]

        if text in commands:
            return self.tools.open_pictures()

        return None

    # =========================
    # Open Music
    # =========================

    def music(self, command):

        text = self.normalize(command)

        commands = [
            "open music",
            "music kholo",
            "music open",
            "মিউজিক খুলো",
        ]

        if text in commands:
            return self.tools.open_music()

        return None

    # =========================
    # Open Videos
    # =========================

    def videos(self, command):

        text = self.normalize(command)

        commands = [
            "open videos",
            "videos kholo",
            "videos open",
            "ভিডিও ফোল্ডার খুলো",
        ]

        if text in commands:
            return self.tools.open_videos()

        return None

    def write_file(self, command):
        # Original command preserve করা হচ্ছে
        original = command.strip()

        patterns = [
            r"^write\s+(.+?)\s+to\s+(.+)$",
            r"^write\s+(.+?)\s+into\s+(.+)$",
            r"^put\s+(.+?)\s+in\s+(.+)$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                original,
                re.IGNORECASE
            )

            if not match:
                continue

            content = match.group(1).strip()
            file_name = match.group(2).strip()

            if not content:
                return "Please provide content."

            if not file_name:
                return "Please provide a file name."

            return self.confirmation.request(
                f"Overwrite {file_name} with new content?",
                lambda: self.tools.write_to_file(
                    file_name,
                    content
                )
            )

        return None


    def append_file(self, command):
        original = command.strip()

        patterns = [
            r"^append\s+(.+?)\s+to\s+(.+)$",
            r"^append\s+(.+?)\s+into\s+(.+)$",
            r"^add\s+(.+?)\s+to\s+(.+)$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                original,
                re.IGNORECASE
            )

            if not match:
                continue

            content = match.group(1).strip()
            file_name = match.group(2).strip()

            if not content:
                return "Please provide content."

            if not file_name:
                return "Please provide a file name."

            return self.tools.append_to_file(
                file_name,
                content
            )

        return None


    def read_file(self, command):
        original = command.strip()

        patterns = [
            r"^read\s+file\s+(.+)$",
            r"^read\s+(.+)$",
            r"^show\s+content\s+of\s+(.+)$",
            r"^show\s+file\s+content\s+(.+)$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                original,
                re.IGNORECASE
            )

            if not match:
                continue

            file_name = match.group(1).strip()

            if not file_name:
                return "Please provide a file name."

            return self.tools.read_file(file_name)

        return None