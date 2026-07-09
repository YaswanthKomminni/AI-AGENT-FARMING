"""
Translation Module — deep-translator wrapper
Supports regional Indian languages
"""
import logging
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

LANGUAGE_CODES = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Odia": "or",
    "Assamese": "as",
    "Urdu": "ur",
    "English": "en",
}


def get_supported_languages() -> list[dict]:
    return [{"name": name, "code": code} for name, code in LANGUAGE_CODES.items()]


def translate_text(text: str, target_language: str = "English", source_language: str = "auto") -> str:
    """Translate text to the target language."""
    target_code = LANGUAGE_CODES.get(target_language, "en")

    if target_code == "en" and source_language == "auto":
        # Check if text contains non-Latin (e.g. Indian script) characters.
        # Range > 0x024F covers Devanagari, Tamil, Telugu, etc.
        # If it has only Latin/ASCII characters, we assume it's already English/romanized and skip translation.
        has_non_latin = any(ord(c) > 0x024F for c in text)
        if not has_non_latin:
            return text

    try:
        translator = GoogleTranslator(source=source_language, target=target_code)
        translated = translator.translate(text)
        return translated or text
    except Exception as e:
        logger.warning(f"Translation failed ({target_language}): {e}")
        return text  # Return original on failure


def detect_language(text: str) -> str:
    """Attempt to detect the language of input text."""
    try:
        from deep_translator import single_detection
        lang_code = single_detection(text, api_key="free")
        # Map code back to name
        for name, code in LANGUAGE_CODES.items():
            if code == lang_code:
                return name
        return "English"
    except Exception:
        return "English"
