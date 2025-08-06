from livekit.plugins import silero

class VADService:
    def __init__(self):
        self.vad = silero.VAD.load()

    def get(self):
        return self.vad
