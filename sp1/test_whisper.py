
from faster_whisper import WhisperModel

# Load the model
print("Loading Faster-Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Model loaded successfully!")

# Give the path of your audio file
audio_path = "test_audio.mp3"

# Convert audio into text
segments, info = model.transcribe(
    audio_path,
    beam_size=5
)

# Collect the generated text
transcribed_text = ""

for segment in segments:
    transcribed_text += segment.text

print("Detected language:", info.language)
print("Recognized text:", transcribed_text)
