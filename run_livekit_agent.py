# run_livekit_agent.py

import asyncio
import os
import google.generativeai as genai

from livekit import connect
from livekit.agents import JobContext, AgentSession, Agent
from livekit.plugins import silero

from app.services.whisper_service import WhisperService
from app.services.tts_service import TTSService

# 👇 Required: Set your API keys and LiveKit URL/token
LIVEKIT_URL = "wss://your-livekit-url"
LIVEKIT_TOKEN = "your_livekit_access_token"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # or hardcode for dev

class VoiceAssistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")

async def entrypoint(ctx: JobContext):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    whisper = WhisperService()
    tts = TTSService()

    session = AgentSession(
        stt=lambda path: whisper.transcribe(path)[0],
        llm=lambda prompt: model.generate_content(prompt).text,
        tts=lambda text: tts.synthesize(text),
        vad=silero.VAD.load()
    )

    await session.start(room=ctx.room, agent=VoiceAssistant())

async def run_agent():
    room = await connect(LIVEKIT_URL, LIVEKIT_TOKEN)
    ctx = JobContext(
        room=room,
        proc=None,
        info=None,
        on_connect=lambda: print("🔗 Connected"),
        on_shutdown=lambda: print("❌ Disconnected"),
        inference_executor=None,
    )
    await entrypoint(ctx)

if __name__ == "__main__":
    asyncio.run(run_agent())
