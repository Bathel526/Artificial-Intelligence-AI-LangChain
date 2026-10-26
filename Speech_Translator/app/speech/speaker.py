import wave
from pathlib import Path
import tempfile
import winsound

from piper import PiperVoice

VOICES_DIR = Path(__file__).parent / "voices"

VOICE_MODELS = {
    "angielski": "en_US-lessac-medium.onnx",
    "niemiecki": "de_DE-thorsten-medium.onnx",
    "hiszpański": "es_ES-sharvard-medium.onnx",
}

_loaded_voices = {}

def speak_text(text: str, language: str) -> None:

    if not text.strip():
        return

    model_name = VOICE_MODELS.get(language.lower())

    if model_name is None:
        raise ValueError(f"Nieobsługiwany język: {language}")

    model_path = VOICES_DIR / model_name

    if not model_path.exists():
        raise FileNotFoundError(f"Nie znalezono modelu:{model_path}")

    if language.lower() not in _loaded_voices:
        _loaded_voices[language.lower()] = PiperVoice.load(str(model_path))

    voice = _loaded_voices[language.lower()]

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav_path = temp_file.name

    try:
        with wave.open(wav_path, "wb") as waf_file:
            voice.synthesize_wav(text, waf_file)

        winsound.PlaySound(wav_path, winsound.SND_FILENAME)

    finally:
        Path(wav_path).unlink(missing_ok=True)