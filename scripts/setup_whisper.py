from faster_whisper import WhisperModel
import os

# Definimos la ruta local
ruta_proyecto = os.getcwd()
destino_modelo = os.path.join(ruta_proyecto, "models", "whisper-large-v3")

print(f"Descargando el cerebro del robot en: {destino_modelo}, tigre 🐯...")

# Al ejecutar esto, Python creará la estructura correcta dentro de tu carpeta
model = WhisperModel(
    "large-v3", 
    device="cpu",        # Usa "cuda" si ya tienes los drivers de NVIDIA listos
    compute_type="int8", # 'int8' es más ligero y rápido para empezar
    download_root=destino_modelo
)

print("¡Mudanza completada! El modelo ya es parte de tu proyecto.")