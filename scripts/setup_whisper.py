from faster_whisper import WhisperModel
import os

# Usamos una ruta más específica para no confundir modelos en el futuro, tigre 🐯
project_path = os.getcwd()
model_size = "small"
destination = os.path.join(project_path, "models", f"whisper-{model_size}")

print(f"Downloading Whisper {model_size}: {destination}...")

# Inicializar el modelo: esto descargará el modelo a la carpeta del proyecto
model = WhisperModel(
    model_size, 
    device="cpu",        # Cambia a 'cuda' si tienes GPU NVIDIA en el lab
    compute_type="int8", # 'int8' es más rápido y ligero
    download_root=destination
)

print(f"Model {model_size} loaded and ready in: {destination}")