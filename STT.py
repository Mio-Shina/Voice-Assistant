import vosk
import sounddevice as sd
import numpy as np

MODEL_PATH = "model"
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

last_recognized_text = ""

def listen() -> str:
    global last_recognized_text

    with sd.InputStream(samplerate=16000, channels=1, blocksize=8000, dtype='int16') as stream:
        stream.start()

        while True:
            data = stream.read(4000)[0]

            data = np.frombuffer(data, dtype=np.int16).tobytes()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                last_recognized_text = result[14:-3]
                if last_recognized_text != "":
                    print(f"Распознано: {last_recognized_text}")
                    return last_recognized_text
#listen()
