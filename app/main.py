import os
import google.generativeai as genai
from livekit.agents import AgentSession, Agent, JobContext
from livekit.plugins import silero
from app.services.whisper_service import WhisperService
from app.services.tts_service import TTSService

class VoiceAssistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")

async def entrypoint(ctx: JobContext):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    whisper = WhisperService()
    tts = TTSService()

    session = AgentSession(
        stt=lambda path: whisper.transcribe(path)[0],
        llm=lambda prompt: model.generate_content(prompt).text,
        tts=lambda text: tts.synthesize(text),
        vad=silero.VAD.load(),
    )

    await session.start(room=ctx.room, agent=VoiceAssistant())
