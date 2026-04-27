import os
import numpy as np
import speech_recognition as sr
from openwakeword.model import Model

# --- TRUCO PARA SILENCIAR EL SPAM DE ALSA ---
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
# --------------------------------------------

# 1. Cargamos el modelo
ruta_jarvis = "/home/ivan/venv/ur5/lib/python3.12/site-packages/openwakeword/resources/models/hey_jarvis_v0.1.onnx"
model = Model([ruta_jarvis])

# 2. Configuración usando SpeechRecognition (Igual que tu Whisper)
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Configuramos el chunk size para openwakeword (1280 frames a 16khz)
CHUNK = 1280

print("\n" + "—"*40)
print(f"👂 ESCUCHANDO A JARVIS 🐯")
print(f"Modelos activos: {list(model.models.keys())}")
print("—"*40 + "\n")

with mic as source:
    # Ajustamos el ruido ambiente como haces en Whisper (opcional, pero útil)
    print("Calibrando ruido de fondo... shhh...")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("¡Listo! Di 'Hey Jarvis'")

    # Extraemos el stream de PyAudio que sr.Microphone ha configurado bien
    stream = mic.stream

    try:
        while True:
            # Leemos el audio igual que antes, pero desde el stream correcto
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_frame = np.frombuffer(data, dtype=np.int16)
            
            # 1. MEDIDOR DE VOLUMEN (Para que veas que funciona)
            volumen = np.max(np.abs(audio_frame))

            # 2. PREDICCIÓN
            prediction = model.predict(audio_frame)

            for wakeword, score in prediction.items():
                print(f"\r🎤 Vol: {volumen:5d} | 🧠 Confianza {wakeword}: {score:.3f}   ", end="")
                
                # Umbral puesto en 0.5
                if score > 0.5:
                    print(f"\n\n🔥 ¡{wakeword.upper()} DETECTADO! (Confianza: {score:.2f})")
                    model.reset()
                    
    except KeyboardInterrupt:
        print("\n\nDesconectando micrófonos...")