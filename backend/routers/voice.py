"""
API Router: Voice — STT + TTS
"""
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import Response

from voice.stt import speech_to_text, LANGUAGE_STT_CODES
from voice.tts import text_to_speech

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/stt")
async def stt_endpoint(
    audio: UploadFile = File(..., description="Audio file (WAV/FLAC)"),
    language: str = Query("English", description="Language name (e.g. Hindi, Tamil)"),
):
    """Convert uploaded audio to text."""
    lang_code = LANGUAGE_STT_CODES.get(language, "en-IN")
    audio_bytes = await audio.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        text = speech_to_text(audio_bytes, language=lang_code)
        if not text:
            raise HTTPException(status_code=422, detail="Could not understand the audio")
        return {"text": text, "language": language}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/tts")
async def tts_endpoint(
    text: str = Query(..., description="Text to convert"),
    language: str = Query("English", description="Language name"),
):
    """Convert text to speech audio (returns MP3 bytes)."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        audio_bytes = text_to_speech(text=text, language=language)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")
