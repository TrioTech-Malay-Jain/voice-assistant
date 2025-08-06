import whisper
import os
import tempfile

class WhisperService:
    def __init__(self, model_size="base",cache_dir="/tmp"):
        os.makedirs(cache_dir, exist_ok=True)
        self.model = whisper.load_model(model_size,download_root=cache_dir)

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path, task="transcribe")
        return result["text"], result["language"]
