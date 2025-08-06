from fastapi import APIRouter, Form
from app.services.tts_service import TTSService

router = APIRouter()
tts = TTSService()

@router.post("/speak")
def speak(text: str = Form(...), lang: str = Form("en")):
    filepath = tts.synthesize(text, lang)
    return {"audio_path": filepath}
