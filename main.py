
from config import INPUT_MODE

import queue
import threading
from core.listener import Listener
from core.speaker import Speaker
from core.brain import Brain
from core.intent import IntentManager
import os
import sys
import time
import subprocess

listener = Listener()
speaker = Speaker()
brain = Brain()
intent_manager = IntentManager(
    speaker,
    brain
)
speech_queue = queue.Queue()


# =========================
# Reload JARVIS
# =========================

def reload_jarvis():

    print("🔄 Reloading JARVIS...")

    try:

        time.sleep(0.3)

        subprocess.Popen(
            [sys.executable, sys.argv[0]],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        return True

    except Exception as e:

        print(f"❌ Reload failed: {e}")

        return False


# =========================
# Process Command
# =========================
def process_command(user_text):

    if not user_text:
        return True

    command = user_text.lower().strip()

    # =========================
    # Switch Input Mode
    # =========================

    voice_commands = [
        "voice mode",
        "switch to voice mode",
        "change to voice mode",
        "voice on",
    ]

    text_commands = [
        "text mode",
        "switch to text mode",
        "change to text mode",
        "text on",
    ]

    if command in voice_commands:

        listener.set_mode("voice")

        speaker.speak("Switching to voice mode.")

        return "SWITCH_VOICE"

    if command in text_commands:

        listener.set_mode("text")

        speaker.speak("Switching to text mode.")

        return "SWITCH_TEXT"

    # Completely close JARVIS
    if listener.is_exit_command(command):

        speaker.speak("Goodbye Tarek.")

        return False

    # Stop listening / sleep mode
    if listener.is_stop_command(command):

        speaker.speak("Okay Tarek. I am going to sleep.")

        return True

    # Local command execution
    command_result = intent_manager.execute(user_text)

    # Restart JARVIS
    if command_result == "__RELOAD_JARVIS__":

        print("🔄 Restarting JARVIS...")

        return "RELOAD"

    if command_result:

        speech_queue.put(command_result)

        return True

    # AI response
    answer = brain.ask(user_text)

    speaker.speak(answer)

    return True



# =========================
# Text Mode
# =========================

def run_text_mode():

    speaker.speak("Hello Tarek. JARVIS is online.")

    while True:

        user_text = listener.listen()

        result = process_command(user_text)

        if result == "SWITCH_VOICE":
            return "VOICE"

        if result == "RELOAD":

            reload_jarvis()

            break

        if not result:

            break


# =========================
# Voice Mode
# =========================

def run_voice_mode():

    speaker.speak("Hello Tarek. JARVIS is online.")

    conversation_mode = False

    while True:

        # --------------------------------------------------
        # Wake-word mode
        # --------------------------------------------------

        if not conversation_mode:

            print("\n💤 Waiting for wake word...")

            user_text = listener.listen()

            if not user_text:
                continue

            command = user_text.lower().strip()

            if listener.is_exit_command(command):

                speaker.speak("Goodbye Tarek.")

                break

            if listener.is_stop_command(command):

                continue

            if not listener.contains_wake_word(command):

                print("💤 Wake word not detected.")

                continue

            command = listener.remove_wake_word(command)

            if command:

                result = process_command(command)

                if result == "SWITCH_TEXT":
                    return "TEXT"

                if result == "RELOAD":

                    reload_jarvis()

                    break

                if not result:

                    break

            else:

                speaker.speak("Yes Tarek?")

            conversation_mode = True

        # --------------------------------------------------
        # Continuous conversation mode
        # --------------------------------------------------

        else:

            print("\n🟢 Conversation mode active.")
            print("💤 Say 'stop listening' to sleep.")

            user_text = listener.listen()

            if not user_text:
                continue

            command = user_text.lower().strip()

            if listener.is_exit_command(command):

                speaker.speak("Goodbye Tarek.")

                break

            if listener.is_stop_command(command):

                speaker.speak("Okay Tarek. I am going to sleep.")

                conversation_mode = False

                continue

            result = process_command(user_text)

            if result == "RELOAD":

                reload_jarvis()

                break


# =========================
# Speech Worker
# =========================

def speech_worker():

    while True:

        text = speech_queue.get()

        if text is None:

            break

        speaker.speak(text)

        speech_queue.task_done()


threading.Thread(
    target=speech_worker,
    daemon=True
).start()


# =========================
# Start JARVIS
# =========================

if __name__ == "__main__":

    current_mode = listener.get_mode()

    while True:

        if current_mode == "text":

            result = run_text_mode()

        else:

            result = run_voice_mode()

        if result == "VOICE":

            current_mode = "voice"
            continue

        if result == "TEXT":

            current_mode = "text"
            continue

        break
