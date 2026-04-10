import speech_recognition as sr
from faster_whisper import WhisperModel
import io
import os

# Model path
model_path = "/home/ivan/proyectos/ur5/models/whisper-large-v3/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120/"


print("Loading model...")

model = WhisperModel(model_path, 
                     device="cpu", # Change to 'cuda' for better performance if an NVIDIA GPU is available
                     compute_type="int8")

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