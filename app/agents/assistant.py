# app/agents/assistant.py

from livekit import agents
from livekit.agents import Agent, AgentSession
from livekit.plugins import silero
from app.services.whisper_service import WhisperService
from app.services.tts_service import TTSService
import google.generativeai as genai
import tempfile

class VoiceAssistant(Agent):
    def __init__(self):
        super().__init__(instructions="You're a helpful assistant.")

async def entrypoint(ctx: agents.JobContext):
    temp_dir = tempfile.mkdtemp()
    session = AgentSession(
        stt=WhisperService(cache_dir=temp_dir),  # Add `cache_dir` param in your class
        llm=lambda prompt: genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt).text,
        tts=TTSService(),
        vad=silero.VAD.load()
    )
    await session.start(room=ctx.room, agent=VoiceAssistant())
