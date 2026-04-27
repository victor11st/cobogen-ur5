from faster_whisper import WhisperModel
import speech_recognition as sr
import io
import os

class Transcriptor:
    def __init__(self, path_model):
        self._model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
            download_root=path_model
        )
        self._recognizer = sr.Recognizer()
        self._mic = sr.Microphone()

    def _capture_audio(self):
        with self._mic as source:
            try:
                return self._recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return None
            

    def _transcritption(self, audio_capturated):
        audio_data = io.BytesIO(audio_capturated)
        segments, info = self._model.transcribe(audio_data,
                                                language="es", 
                                                beam_size=5,
                                                vad_filter=True)
        
        text_task =  "".join([segment.text for segment in segments])
        return text_task.strip()
    
    def run_listen(self):
        audio = self._capture_audio()

        if audio:
            text = self._transcritption()
            return text
        else:
            return None