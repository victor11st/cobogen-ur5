import os
import numpy as np
import pyaudio
from openwakeword.model import Model

# 1. Cargamos SOLO el modelo de Jarvis de tu carpeta para ser profesionales
ruta_jarvis = os.path.abspath("../models/wakewords/hey_jarvis_v0.1.onnx")

# Pasamos la ruta en una lista, sin nombres de argumentos raros
# Así cargamos solo UN modelo y ahorramos memoria
model = Model([ruta_jarvis]) 

# 2. Configuración de audio
CHUNK = 1280
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNK)

print(f"\n✅ UR5 listo. Palabra clave activa: {list(model.models.keys())}")

try:
    print("\nHabla ahora para probar el micrófono...")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frame = np.frombuffer(data, dtype=np.int16)

        # 1. MEDIDOR DE VOLUMEN
        # Calculamos el pico de volumen de este fragmento de audio
        volumen = np.max(np.abs(audio_frame))

        # 2. PREDICCIÓN DE LA IA
        prediction = model.predict(audio_frame)

        for wakeword, score in prediction.items():
            # Esto imprimirá en la MISMA línea el volumen y la confianza todo el rato
            print(f"\r🎤 Volumen: {volumen:5d} | 🧠 Confianza {wakeword}: {score:.3f}   ", end="")
            
            # Hemos bajado el umbral a 0.4 para probar
            if score > 0.4:
                print(f"\n\n🔥 ¡{wakeword.upper()} DETECTADO! (Confianza: {score:.2f})")
                model.reset() 
                
except KeyboardInterrupt:
    print("\nDesconectando micrófonos...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()