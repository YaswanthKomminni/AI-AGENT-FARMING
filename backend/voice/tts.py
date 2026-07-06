"""
Voice Module: Text-to-Speech
"""
import io
import logging
from gtts import gTTS
from translation.translator import LANGUAGE_CODES

logger = logging.getLogger(__name__)


def text_to_speech(text: str, language: str = "English") -> bytes:
    """Convert text to speech audio bytes (MP3)."""
    lang_code = LANGUAGE_CODES.get(language, "en")

    # Truncate for TTS if too long
    if len(text) > 2000:
        text = text[:2000] + "..."

    # Strip markdown symbols that sound bad in TTS
    clean = (
        text.replace("**", "").replace("*", "").replace("#", "")
            .replace("`", "").replace("🌾", "").replace("⚠️", "Warning:")
            .replace("✅", "").replace("🔴", "").replace("🟡", "")
    )

    tts = gTTS(text=clean, lang=lang_code, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()
