import json
import os


class MemoryManager:

    def __init__(self):

        self.memory_dir = os.path.join(
            os.getcwd(),
            "memory"
        )

        self.memory_file = os.path.join(
            self.memory_dir,
            "memory.json"
        )

        os.makedirs(
            self.memory_dir,
            exist_ok=True
        )

        if not os.path.exists(self.memory_file):

            self.save_memory({})


    def load_memory(self):

        try:

            with open(
                self.memory_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            return {}


    def save_memory(self, data):

        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )


    def remember(self, key, value):

        key = key.strip().lower()
        value = value.strip()

        memory = self.load_memory()

        memory[key] = value

        self.save_memory(memory)

        return f"I'll remember that your {key} is {value}."


    def get(self, key):

        key = key.strip().lower()

        memory = self.load_memory()

        return memory.get(key)


    def forget(self, key):

        key = key.strip().lower()

        memory = self.load_memory()

        if key not in memory:

            return f"I don't have {key} in my memory."

        del memory[key]

        self.save_memory(memory)

        return f"I forgot your {key}."


    def all_memory(self):

        return self.load_memory()


    def remember_sentence(self, sentence):

        sentence = sentence.strip()

        patterns = [
            ("i live in ", "location"),
            ("i am from ", "location"),
            ("my manager's name is ", "manager name"),
            ("my manager name is ", "manager name"),
            ("my favorite browser is ", "favorite browser"),
            ("my favorite programming language is ", "favorite programming language"),
            ("my favorite language is ", "favorite language"),
        ]

        lower_sentence = sentence.lower()

        for prefix, key in patterns:

            if lower_sentence.startswith(prefix):

                value = sentence[len(prefix):].strip()

                if value:
                    return self.remember(
                        key,
                        value
                    )

        return None