import os
import shutil
from datetime import datetime
from send2trash import send2trash

def get_user_path(folder_name):
    """
    Get a folder path from the user's home directory.
    """

    return os.path.join(
        os.path.expanduser("~"),
        folder_name
    )


# =========================
# Open Folders
# =========================

def open_desktop():

    path = get_user_path("Desktop")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Desktop."

    return "Desktop folder was not found."


def open_downloads():

    path = get_user_path("Downloads")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Downloads."

    return "Downloads folder was not found."


def open_documents():

    path = get_user_path("Documents")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Documents."

    return "Documents folder was not found."


def open_pictures():

    path = get_user_path("Pictures")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Pictures."

    return "Pictures folder was not found."


def open_music():

    path = get_user_path("Music")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Music."

    return "Music folder was not found."


def open_videos():

    path = get_user_path("Videos")

    if os.path.exists(path):
        os.startfile(path)
        return "Opening Videos."

    return "Videos folder was not found."


# =========================
# Create Folder
# =========================
def create_folder(folder_name, location=None):
    folder_name = folder_name.strip()

    if not folder_name:
        return "Please provide a folder name."

    if location:
        location = os.path.expandvars(
            os.path.expanduser(location.strip())
        )
    else:
        location = os.path.expanduser("~")

    path = os.path.join(location, folder_name)

    if os.path.exists(path):
        return f"The folder {folder_name} already exists at {path}."

    try:
        os.makedirs(path, exist_ok=True)

        return f"Folder {folder_name} created at {path}."

    except Exception as e:
        return f"Could not create folder: {e}"


# =========================
# Create Text File
# =========================

def create_text_file(file_name, location=None, content=""):
    file_name = file_name.strip()

    if not file_name:
        return "Please provide a file name."

    if not file_name.lower().endswith(".txt"):
        file_name += ".txt"

    if location:
        location = os.path.expandvars(
            os.path.expanduser(location.strip())
        )
    else:
        location = get_user_path("Desktop")

    try:
        os.makedirs(location, exist_ok=True)

        path = os.path.join(location, file_name)

        if os.path.exists(path):
            return f"The file {file_name} already exists at {path}."

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return f"File {file_name} created at {path}."

    except Exception as e:
        return f"Could not create file: {e}"


# =========================
# Rename File / Folder
# =========================

def rename_item(old_name, new_name):

    search_locations = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Pictures"),
        os.path.join(os.path.expanduser("~"), "Music"),
        os.path.join(os.path.expanduser("~"), "Videos"),
    ]

    matches = []

    for location in search_locations:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            # File match
            for file in files:

                if file.lower() == old_name.lower():

                    matches.append(
                        os.path.join(root, file)
                    )

            # Folder match
            for directory in dirs:

                if directory.lower() == old_name.lower():

                    matches.append(
                        os.path.join(root, directory)
                    )


    if not matches:

        return f"{old_name} was not found."


    if len(matches) > 1:

        result = f"I found multiple items named {old_name}:\n"

        for index, path in enumerate(matches[:10], 1):

            result += f"{index}. {path}\n"

        return result.strip()


    old_path = matches[0]

    directory = os.path.dirname(old_path)

    new_path = os.path.join(
        directory,
        new_name
    )


    if os.path.exists(new_path):

        return f"{new_name} already exists."


    try:

        os.rename(
            old_path,
            new_path
        )

        return (
            f"Renamed {old_name} to {new_name}."
        )

    except Exception as e:

        return f"Could not rename {old_name}: {e}"


# =========================
# Move File / Folder
# =========================

def move_item(item_name, destination_folder):

    item_name = item_name.strip()
    destination_folder = destination_folder.strip()

    desktop = get_user_path("Desktop")
    destination = get_user_path(destination_folder)

    source = os.path.join(
        desktop,
        item_name
    )

    if not os.path.exists(source):
        return f"{item_name} was not found on Desktop."

    if not os.path.exists(destination):
        return f"{destination_folder} folder was not found."

    try:

        shutil.move(
            source,
            destination
        )

        return (
            f"Moved {item_name} "
            f"to {destination_folder}."
        )

    except Exception as e:

        return f"Could not move item: {e}"

# =========================
# Search Files / Folders
# =========================

def search_files(search_name):

    search_name = search_name.strip().lower()

    if not search_name:
        return "Please provide a file or folder name."

    search_locations = [
        os.path.expanduser("~"),
        get_user_path("Desktop"),
        get_user_path("Documents"),
        get_user_path("Downloads"),
        get_user_path("Pictures"),
        get_user_path("Music"),
        get_user_path("Videos"),
    ]

    results = []
    checked_paths = set()

    for location in search_locations:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            # Avoid duplicate locations
            real_root = os.path.abspath(root)

            if real_root in checked_paths:
                continue

            checked_paths.add(real_root)

            # Search folders
            for folder in dirs:

                if search_name in folder.lower():

                    path = os.path.join(
                        root,
                        folder
                    )

                    if path not in results:
                        results.append(path)

            # Search files
            for file in files:

                if search_name in file.lower():

                    path = os.path.join(
                        root,
                        file
                    )

                    if path not in results:
                        results.append(path)

            # Prevent too many results
            if len(results) >= 20:
                break

        if len(results) >= 20:
            break

    if not results:
        return f"I could not find {search_name}."

    print("\n🔎 Search Results:")

    for index, path in enumerate(results, start=1):

        print(f"{index}. {path}")

    # If only one result, open automatically
    if len(results) == 1:

        try:
            os.startfile(results[0])

            return f"I found and opened {search_name}."

        except Exception:
            return f"I found {search_name}: {results[0]}"

    return (
        f"I found {len(results)} results for "
        f"{search_name}. Check the search results."
    )


# =========================
# Open Specific Path
# =========================

def open_path(path):

    path = os.path.expandvars(
        os.path.expanduser(path.strip())
    )

    if not os.path.exists(path):
        return f"I could not find {path}."

    try:

        os.startfile(path)

        return f"Opening {path}."

    except Exception as e:

        return f"Could not open {path}: {e}"


# =========================
# File Information
# =========================

def get_file_info(file_name):

    file_name = file_name.strip()

    if not file_name:
        return "Please provide a file name."

    search_locations = [
        get_user_path("Desktop"),
        get_user_path("Documents"),
        get_user_path("Downloads"),
    ]

    found_path = None

    for location in search_locations:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            for file in files:

                if file.lower() == file_name.lower():

                    found_path = os.path.join(
                        root,
                        file
                    )

                    break

            if found_path:
                break

        if found_path:
            break

    if not found_path:
        return f"I could not find {file_name}."

    try:

        size = os.path.getsize(found_path)

        modified = os.path.getmtime(found_path)

        modified_date = datetime.fromtimestamp(
            modified
        ).strftime("%d %B %Y %I:%M %p")

        if size < 1024:

            size_text = f"{size} bytes"

        elif size < 1024 * 1024:

            size_text = f"{size / 1024:.2f} KB"

        else:

            size_text = f"{size / (1024 * 1024):.2f} MB"

        print("\n📄 File Information")
        print(f"Name     : {file_name}")
        print(f"Location : {found_path}")
        print(f"Size     : {size_text}")
        print(f"Modified : {modified_date}")

        return (
            f"{file_name} is {size_text}. "
            f"It was last modified on {modified_date}."
        )

    except Exception as e:

        return f"Could not read file information: {e}"


# =========================
# Recent Files
# =========================

def get_recent_files():

    locations = [
        get_user_path("Desktop"),
        get_user_path("Documents"),
        get_user_path("Downloads"),
    ]

    files = []

    for location in locations:

        if not os.path.exists(location):
            continue

        for root, dirs, filenames in os.walk(location):

            for filename in filenames:

                path = os.path.join(
                    root,
                    filename
                )

                try:

                    modified_time = os.path.getmtime(path)

                    files.append(
                        (
                            modified_time,
                            path
                        )
                    )

                except OSError:
                    continue

    files.sort(
        key=lambda item: item[0],
        reverse=True
    )

    recent_files = files[:10]

    if not recent_files:

        return "I could not find any recent files."

    print("\n🕐 Recent Files:")

    for index, (modified_time, path) in enumerate(
        recent_files,
        start=1
    ):

        modified_date = datetime.fromtimestamp(
            modified_time
        ).strftime("%d %b %Y %I:%M %p")

        print(
            f"{index}. {os.path.basename(path)}"
            f" | {modified_date}"
        )
        print(f"   {path}")

    return (
        f"I found {len(recent_files)} recent files. "
        f"Check the list in the terminal."
    )

def delete_item(item_name):

    # ==========================================
    # Exact path support
    # ==========================================

    if os.path.exists(item_name):

        try:

            send2trash(item_name)

            return (
                f"Deleted {os.path.normpath(item_name)}."
            )

        except Exception as e:

            return (
                f"Could not delete "
                f"{os.path.normpath(item_name)}: {e}"
            )

    # ==========================================
    # Fallback: search common user folders
    # ==========================================

    home = os.path.expanduser("~")

    search_locations = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Pictures"),
        os.path.join(home, "Music"),
        os.path.join(home, "Videos"),
    ]

    for folder in search_locations:

        item_path = os.path.join(
            folder,
            item_name
        )

        if os.path.exists(item_path):

            try:

                send2trash(item_path)

                return (
                    f"{item_name} was moved to the Recycle Bin."
                )

            except Exception as e:

                return (
                    f"Could not delete {item_name}: {e}"
                )

    return f"Could not find {item_name}."

def empty_recycle_bin():

    try:

        import ctypes

        result = ctypes.windll.shell32.SHEmptyRecycleBinW(
            None,
            None,
            0
        )

        if result == 0:
            return "Recycle Bin has been emptied."

        return "Could not empty the Recycle Bin."

    except Exception as e:

        return f"Could not empty the Recycle Bin: {e}"

def find_existing_file(file_name):
    """
    Find an existing file by:
    1. Exact/full path
    2. Common user folders
    """

    file_name = file_name.strip()

    # Full/direct path
    direct_path = os.path.expandvars(
        os.path.expanduser(file_name)
    )

    if os.path.isfile(direct_path):
        return direct_path

    # Common folders
    search_locations = [
        os.path.expanduser("~"),
        get_user_path("Desktop"),
        get_user_path("Documents"),
        get_user_path("Downloads"),
        get_user_path("Pictures"),
        get_user_path("Music"),
        get_user_path("Videos"),
    ]

    for location in search_locations:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            for file in files:

                if file.lower() == file_name.lower():

                    return os.path.join(
                        root,
                        file
                    )

    return None


def write_to_file(file_name, content):
    """
    Replace existing file content.
    """

    file_name = file_name.strip()

    if not file_name:
        return "Please provide a file name."

    path = find_existing_file(file_name)

    if not path:
        return f"I couldn't find the file {file_name}."

    try:

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return f"Content written to {os.path.basename(path)}."

    except Exception as e:

        return f"Could not write to file: {e}"


def append_to_file(file_name, content):
    """
    Add content to the end of an existing file.
    """

    file_name = file_name.strip()

    if not file_name:
        return "Please provide a file name."

    path = find_existing_file(file_name)

    if not path:
        return f"I couldn't find the file {file_name}."

    try:

        with open(path, "a", encoding="utf-8") as file:

            # Add newline before appended content
            if os.path.getsize(path) > 0:
                file.write("\n")

            file.write(content)

        return f"Content appended to {os.path.basename(path)}."

    except Exception as e:

        return f"Could not append to file: {e}"


def read_file(file_name):
    """
    Read content from an existing text file.
    """

    file_name = file_name.strip()

    if not file_name:
        return "Please provide a file name."

    path = find_existing_file(file_name)

    if not path:
        return f"I couldn't find the file {file_name}."

    try:

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            return f"{os.path.basename(path)} is empty."

        return (
            f"Content of {os.path.basename(path)}:\n"
            f"{content}"
        )

    except Exception as e:

        return f"Could not read file: {e}"