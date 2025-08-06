from gtts import gTTS
import uuid
import os

class TTSService:
    def __init__(self, output_dir="/tmp"):
        self.output_dir = output_dir

    def synthesize(self, text, lang="en"):
        filename = os.path.join(self.output_dir, f"tts_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text=text, lang=lang if lang in ["en", "hi"] else "en")
        tts.save(filename)
        return filename
