from fastapi import APIRouter, File, UploadFile
from app.services.whisper_service import WhisperService

router = APIRouter()
whisper = WhisperService()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with open("temp_audio.webm", "wb") as f:
        f.write(await file.read())

    text, lang = whisper.transcribe("temp_audio.webm")
    return {"text": text, "language": lang}
