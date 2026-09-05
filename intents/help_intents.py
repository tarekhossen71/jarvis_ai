class HelpIntents:

    def __init__(self, normalize):
        self.normalize = normalize

    def help(self, text):
        text = self.normalize(text)

        commands = [
            "what can you do",
            "what can you do jarvis",
            "show commands",
            "show my commands",
            "list commands",
            "available commands",
            "help",
            "jarvis help",
            "কি কি করতে পারো",
            "তুমি কি করতে পারো",
            "কমান্ড দেখাও",
        ]

        if text not in commands:
            return None

        return """
I can help you with these commands:

Browser:
- Open YouTube
- Open Google
- Search Google
- Search YouTube

Applications:
- Open Notepad
- Open Calculator
- Open Chrome
- Open VS Code
- Close applications
- Minimize all windows
- Show desktop

Files and folders:
- Open Desktop
- Open Downloads
- Create a folder
- Create a file
- Search files
- Rename a file
- Move a file
- Delete a file
- Show recent files
- Show file information

Memory:
- Remember information
- Recall information
- Show saved memories
- Forget saved information

System:
- Shutdown PC
- Restart PC
- Stop listening
- Bye

You can also ask me normal questions using Gemini.
""".strip()

    def smart_help(self, text):
        text = self.normalize(text)

        result = self.help(text)

        if result:
            return result

        if any(keyword in text for keyword in [
            "what can you do with file",
            "what can you do with files",
            "what can you do with folder",
            "what can you do with folders",
            "file related commands",
            "folder related commands",
            "ফাইল দিয়ে কি করতে পারো",
            "ফোল্ডার দিয়ে কি করতে পারো",
        ]):
            return """
For files and folders, I can:

- Create a folder
- Create a file
- Search files
- Open a file or folder
- Rename a file
- Move a file
- Delete a file
- Show recent files
- Show file information
""".strip()

        if any(keyword in text for keyword in [
            "what can you do with app",
            "what can you do with application",
            "what can you do with software",
            "app related commands",
            "application related commands",
            "অ্যাপ দিয়ে কি করতে পারো",
        ]):
            return """
For applications, I can:

- Open Notepad
- Open Calculator
- Open Chrome
- Open VS Code
- Open CMD
- Close applications
- Minimize all windows
- Show desktop
""".strip()

        if any(keyword in text for keyword in [
            "what can you do with memory",
            "memory related commands",
            "what can you remember",
            "মেমোরি দিয়ে কি করতে পারো",
        ]):
            return """
For memory, I can:

- Remember information
- Recall information
- Show saved memories
- Forget saved information
""".strip()

        if any(keyword in text for keyword in [
            "what can you do with system",
            "system related commands",
            "what can you do with computer",
            "computer related commands",
            "সিস্টেম দিয়ে কি করতে পারো",
        ]):
            return """
For system control, I can:

- Shutdown the PC
- Restart the PC
- Stop listening
- Exit JARVIS
""".strip()

        return None