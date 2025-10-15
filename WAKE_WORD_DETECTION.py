from pvrecorder import PvRecorder
import pvporcupine

def wake_word_detection(access_key, keyword_paths, keywords) -> bool:
    porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths, keywords=keywords)
    recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

    try:
        recoder.start()

        while True:
            keyword_index = porcupine.process(recoder.read())
            if keyword_index >= 0:
                print(f"Обнаружено {keywords[keyword_index]}")
                return True

    except KeyboardInterrupt:
        recoder.stop()

    finally:
        porcupine.delete()  
