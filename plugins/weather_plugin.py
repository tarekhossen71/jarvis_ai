def weather(command):

    return "Hello! This is the weather plugin."


def get_plugin():

    return {
        "name": "weather",

        "description": "Custom weather plugin.",

        "keywords": [
            "weather plugin",
        ],

        "function": weather,

        "enabled": True,
    }
