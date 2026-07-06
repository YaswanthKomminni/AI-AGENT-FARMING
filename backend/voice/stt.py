"""
Voice Module: Speech-to-Text using SpeechRecognition
"""
import io
import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)


def speech_to_text(audio_bytes: bytes, language: str = "en-IN") -> str:
    """Convert audio bytes (WAV/FLAC) to text using Google STT."""
    recognizer = sr.Recognizer()

    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language=language)
        logger.info(f"STT recognised: '{text[:50]}'")
        return text
    except sr.UnknownValueError:
        logger.warning("STT: Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"STT service error: {e}")
        raise RuntimeError(f"Speech recognition service error: {e}")


LANGUAGE_STT_CODES = {
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Malayalam": "ml-IN",
    "Odia": "or-IN",
    "English": "en-IN",
}
