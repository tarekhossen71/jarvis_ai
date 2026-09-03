from core.listener import Listener
from core.speaker import Speaker
from core.brain import JarvisBrain
from core.intent import IntentManager


listener = Listener()
speaker = Speaker()
brain = JarvisBrain()
intent_manager = IntentManager()


def process_command(user_text):

    if not user_text:
        return True

    command = user_text.lower().strip()

    # Exit JARVIS completely
    if listener.is_exit_command(command):

        speaker.speak("Goodbye Tarek.")

        return False

    # Stop current listening session
    if listener.is_stop_command(command):

        speaker.speak("Okay Tarek. I am going to sleep.")

        return True

    # Execute local command
    command_result = intent_manager.execute(user_text)

    if command_result:

        speaker.speak(command_result)

        return True

    # Ask Gemini
    answer = brain.ask(user_text)

    speaker.speak(answer)

    return True


def run_text_mode():

    while True:

        user_text = listener.listen()

        if not process_command(user_text):
            break


def run_voice_mode():

    speaker.speak("Hello Tarek. JARVIS is online.")

    conversation_mode = False

    while True:

        if conversation_mode:

            print("\n🟢 Conversation mode active.")
            print("💤 Say 'stop listening' to sleep.")

            user_text = listener.listen()

            if not user_text:
                continue

            command = user_text.lower().strip()

            # Exit JARVIS completely
            if listener.is_exit_command(command):

                speaker.speak("Goodbye Tarek.")

                break

            # Stop conversation mode
            if listener.is_stop_command(command):

                speaker.speak("Okay Tarek. I am going to sleep.")

                conversation_mode = False

                continue

            # Execute command or ask AI
            process_command(user_text)

            continue

        # Wake-word waiting mode
        print("\n💤 Waiting for wake word...")

        wake_text = listener.listen()

        if not wake_text:
            continue

        wake_text = wake_text.lower().strip()

        # Exit without wake word
        if listener.is_exit_command(wake_text):

            speaker.speak("Goodbye Tarek.")

            break

        # Ignore stop command when already sleeping
        if listener.is_stop_command(wake_text):

            continue

        # Wake word not detected
        if not listener.contains_wake_word(wake_text):

            print("💤 Wake word not detected.")

            continue

        # Remove wake word
        command = listener.remove_wake_word(wake_text)

        # Example: Hey Jarvis, open YouTube
        if command:

            if not process_command(command):
                break

        else:

            speaker.speak("Yes Tarek?")

        # Activate continuous conversation
        conversation_mode = True

if __name__ == "__main__":

    if listener.__class__.__module__:

        from config import INPUT_MODE

        if INPUT_MODE.lower() == "text":

            run_text_mode()

        else:

            run_voice_mode()