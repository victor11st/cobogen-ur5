from faster_whisper import WhisperModel
import os

# Define the local path for model storage
project_path = os.getcwd()
destination = os.path.join(project_path, "models", "whisper-large-v3")

print(f"Downloading Whisper: {destination}...")

# Initialize Whisper: This will download the model to the project folder if not present
model = WhisperModel(
    "small", 
    device="cpu",        # Change to 'cuda' for better performance if an NVIDIA GPU is available
    compute_type="int8", # 'int8' faster and lighter (requires less RAM/VRAM)
    download_root=destination
)

print("Model loaded and ready in the local project directory.")