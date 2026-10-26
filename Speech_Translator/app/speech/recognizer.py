import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

def record_audio() -> np.ndarray:

    audio_chunks = []

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Informacja o nagrywaniu: {status}")

        audio_chunks.append(indata.copy())

    print("\nNagrywanie rozpoczęte!")
    print("Mów po polsku. Naciśnij Enter, aby zakończyć nagrywanie.")

    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="float32",
        callback=audio_callback,
    ):
        input()

    if not audio_chunks:
        raise RuntimeError("Nie nagrano żadnego dźwięku.")

    return np.concatenate(audio_chunks, axis=0).flatten()

def transcribe_audio(audio: np.ndarray) -> str:

    segments, info = whisper_model.transcribe(
        audio,
        language="pl",
        vad_filter=True,
    )

    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()