import speech_recognition as sr
from faster_whisper import WhisperModel
import io
import os

# Ruta al modelo que descargaste anteriormente
model_path = "/home/ivan/proyectos/ur5/models/whisper-large-v3/models--Systran--faster-whisper-large-v3/snapshots/edaa852ec7e145841d8ffdb056a99866b5f0a478"

# Inicializar el modelo
# Si tienes una tarjeta NVIDIA, usa device="cuda" y compute_type="float16"
# Para probar solo con procesador, usa device="cpu" y compute_type="int8"
print("Cargando modelo de IA...")
model = WhisperModel(model_path, device="cpu", compute_type="int8")

def realizar_prueba():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("\n--- CONFIGURACIÓN ---")
        print("Ajustando ruido ambiente. Por favor, mantén silencio un momento...")
        # recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ajuste completado.")
        
        print("\n--- ESCUCHANDO ---")
        print("Di algo en español (ejemplo: 'Mueve el robot a la derecha')")

        try:
            while True:
                # El sistema escucha hasta detectar un silencio significativo
                audio = recognizer.listen(source, phrase_time_limit=10)
                
                # Convertir el audio capturado a un formato compatible con Whisper
                audio_data = io.BytesIO(audio.get_wav_data())
                
                # Procesar el audio con el modelo
                segments, info = model.transcribe(audio_data, language="es", beam_size=5)
                
                # Imprimir los resultados
                for segment in segments:
                    print(f"[{info.language}] Texto detectado: {segment.text}")
                
                print("Escuchando de nuevo... (Presiona Ctrl+C para salir)")

        except KeyboardInterrupt:
            print("\nPrueba finalizada por el usuario.")

if __name__ == "__main__":
    realizar_prueba()