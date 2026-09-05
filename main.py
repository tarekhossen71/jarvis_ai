from config import INPUT_MODE

import queue
import threading
from core.listener import Listener
from core.speaker import Speaker
from core.brain import Brain
from core.intent import IntentManager


listener = Listener()
speaker = Speaker()
brain = Brain()
intent_manager = IntentManager(speaker)
speech_queue = queue.Queue()


def process_command(user_text):

    if not user_text:
        return True

    command = user_text.lower().strip()

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

    if command_result:

        # speaker.speak(command_result)
        speech_queue.put(command_result)

        return True

    # AI response
    answer = brain.ask(user_text)

    speaker.speak(answer)

    return True


def run_text_mode():

    speaker.speak("Hello Tarek. JARVIS is online.")

    while True:

        user_text = listener.listen()

        if not process_command(user_text):

            break


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

            # Exit without wake word
            if listener.is_exit_command(command):

                speaker.speak("Goodbye Tarek.")

                break

            # Ignore stop command while sleeping
            if listener.is_stop_command(command):

                continue

            # Ignore normal speech without wake word
            if not listener.contains_wake_word(command):

                print("💤 Wake word not detected.")

                continue

            # Remove "Hey Jarvis"
            command = listener.remove_wake_word(command)

            # Example: Hey Jarvis, open YouTube
            if command:

                if not process_command(command):

                    break

            # Example: Hey Jarvis
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

            # Exit completely
            if listener.is_exit_command(command):

                speaker.speak("Goodbye Tarek.")

                break

            # Return to wake-word mode
            if listener.is_stop_command(command):

                speaker.speak("Okay Tarek. I am going to sleep.")

                conversation_mode = False

                continue

            # Execute command or ask Gemini
            process_command(user_text)



speaker = Speaker()

speech_queue = queue.Queue()


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

if __name__ == "__main__":

    if INPUT_MODE.lower() == "text":

        run_text_mode()

    else:

        run_voice_mode()