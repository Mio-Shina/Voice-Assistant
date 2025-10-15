import time
import sounddevice as sd
import torch
import soundfile as sf

language = 'ru'
model_id = 'v4_ru'
sample_rate = 48000
speaker = 'kseniya'
put_accent = True
put_yo = True
device = torch.device('cpu')

if 'model' not in globals():
    model = torch.hub.load(repo_or_dir='snakers4/silero-models',
                           model='silero_tts',
                           language=language,
                           speaker=model_id)[0]
    model.to(device)

def va_speak(what: str):
    audio = model.apply_tts(text=what + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()


'''def generate_voice_file(text: str, output_file: str):
    audio = model.apply_tts(text=text + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sf.write(output_file, audio, sample_rate)
    print(f"Audio saved as {output_file}")'''
