import g4f
import tts

def ask_gpt(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_long,
        messages=messages)
    tts.va_speak(response)
    print(f'[log]: {response}')
    return response

