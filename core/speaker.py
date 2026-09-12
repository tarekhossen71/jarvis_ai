
import asyncio
import os
import uuid

import edge_tts
from playsound import playsound


class Speaker:

    def __init__(self):

        # Natural Microsoft neural voice
        self.voice = "en-US-ChristopherNeural"

        self.rate = "-5%"
        self.volume = "+0%"

    async def _generate_audio(self, text, filename):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume
        )

        await communicate.save(filename)

    def speak(self, text):

        print(f"🤖 JARVIS: {text}")

        filename = os.path.join(
            os.getcwd(),
            f"jarvis_{uuid.uuid4().hex}.mp3"
        )

        try:

            # Generate audio
            asyncio.run(
                self._generate_audio(
                    text,
                    filename
                )
            )

            # Play audio
            try:

                playsound(filename)

            except Exception as e:

                print(f"🔊 Playback Error: {e}")

        except Exception as e:

            print(f"🔊 TTS Error: {e}")

        finally:

            # Give Windows/COM a moment to release the file
            try:

                if os.path.exists(filename):

                    os.remove(filename)

            except Exception:

                pass
