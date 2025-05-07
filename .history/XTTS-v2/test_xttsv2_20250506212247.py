from TTS.api import TTS

# Path to your local XTTS-v2 model directory
MODEL_PATH = "."

# Example text to synthesize
text = "Hello, this is XTTS-v2 running locally!"

# Output file
output_path = "output.wav"

tts = TTS(model_path=MODEL_PATH, progress_bar=True, gpu=False)
tts.tts_to_file(text=text, file_path=output_path)
print(f"Audio saved to {output_path}")
