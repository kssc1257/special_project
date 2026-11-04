
from faster_whisper import WhisperModel

# Load the model only once when this module is imported
print("Loading Faster-Whisper...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Faster-Whisper is ready!")


def transcribe_audio(audio_path):

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True
    )

    # The segments object is a generator.
    # Iterating over it actually performs transcription.
    text = ""

    for segment in segments:
        text += segment.text

    return {
        "text": text.strip(),
        "language": info.language
    }
