import os
import numpy as np
import speech_recognition as sr
from openwakeword.model import Model

class DectectorJarvis:
    _CHUNK = 1280
    def __init__(self, path_model):
        self._model = Model([path_model])
        self._recognizer = sr.Recognizer()
        self._mic = sr.Microphone(sample_rate=16000, chunk_size=DectectorJarvis._CHUNK)


    def run_listen(self, threshold = 0.5):
        with self._mic as source:
            while True:
                audio_chunk = source.stream.read(DectectorJarvis._CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(audio_chunk, dtype=np.int16)

                prediction = self._model.predict(audio_data)

                for mode_name, score in prediction.items():
                    if score > threshold:
                        return True