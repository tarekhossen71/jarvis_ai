import json
import re


class TaskPlanner:

    def __init__(self, brain):
        self.brain = brain

    def create_plan(self, user_request):

        if not user_request:
            return None

        prompt = f"""
You are the autonomous planning engine of JARVIS.

Your job is to understand the user's goal and create an
executable multi-step plan.

USER REQUEST:
{user_request}

IMPORTANT RULES:

1. Do NOT execute anything.
2. Do NOT invent real filesystem paths.
3. Do NOT invent files that do not exist.
4. Use natural descriptions for locations.
5. Break complex requests into small steps.
6. Simple requests may have one step.
7. Each step must describe exactly what JARVIS should do.
8. The executor will resolve real paths locally.
9. Return ONLY valid JSON.

AVAILABLE ACTIONS:

Files:
- create_folder
- create_file
- open_file
- search_file
- rename_file

Applications:
- open_app
- close_app

Browser:
- open_website
- google_search
- youtube_search

System:
- get_time
- get_date
- system_status
- battery
- cpu_usage
- ram_usage

Volume:
- set_volume
- increase_volume
- decrease_volume
- mute_volume
- unmute_volume

Other:
- screenshot
- read_clipboard
- clear_clipboard

IMPORTANT:
Use only actions from this list.

For locations such as:
- project folder
- desktop
- downloads
- documents
- pictures

DO NOT create an absolute Windows path.

The local JARVIS resolver will find the real path.

JSON FORMAT:

{{
    "goal": "short description of the user's goal",
    "steps": [
        {{
            "step": 1,
            "action": "action name",
            "description": "what JARVIS should do",
            "parameters": {{}}
        }}
    ]
}}

USER REQUEST:
{user_request}
"""

        try:

            response = self.brain.client.models.generate_content(
                model=self.brain.model_name,
                contents=prompt
            )

            text = response.text.strip()

            return self._extract_json(text)

        except Exception as e:

            print(f"❌ Planner error: {e}")

            return None

    # ============================================================
    # EXTRACT JSON
    # ============================================================

    def _extract_json(self, text):

        if not text:
            return None

        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

        text = text.strip()

        try:

            return json.loads(text)

        except json.JSONDecodeError:
            pass

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return None

        try:

            return json.loads(
                text[start:end + 1]
            )

        except json.JSONDecodeError:

            return None