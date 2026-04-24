import speech_recognition as sr
from faster_whisper import WhisperModel
import io
import os


print("Loading model...")

# Definimos tu carpeta base de modelos
carpeta_modelos = "/home/ivan/proyectos/ur5/models/whisper-large-v3/"

# Le decimos a faster-whisper que queremos el modelo "small".
# Él se encargará de descargarlo limpio (o usarlo si está sano) en esa carpeta.
model = WhisperModel(
    "small", 
    device="cpu", 
    compute_type="int8",
    download_root=carpeta_modelos
)
def test_model():

    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("model loaded successfully")
    with mic as source:
        print("\n--- CONFIGURATION ---")
        print("Adjusting ambient noise... Please stay silent for a moment.")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Adjustment completed.")
        
        print("\n--- Listening ---")
        print("Speak spanish")

        try:
            while True:
                try:
                    # The system listens until silence is detected
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Convert capture audio to compatible format whith Whisper
                    audio_data = io.BytesIO(audio.get_wav_data())
                    
                    # Procesar el audio con el modelo
                    # Precess audio with model
                    segments, info = model.transcribe(audio_data, 
                                                    language="es", 
                                                    beam_size=5,
                                                    vad_filter=True)
                    
                    # Print result
                    for segment in segments:
                        print(f"[{info.language}] Text detected: {segment.text}")
                except sr.WaitTimeoutError:
                    print(" No speech detected")
                
                print("Listening again... (Press Ctrl+C fot exit)")

        except KeyboardInterrupt:
            print("\nTest finished.")

if __name__ == "__main__":
    test_model()