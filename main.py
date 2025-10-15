from pydub import AudioSegment
from pydub.playback import play

import stt
import tts
import wiki
import config
import cmd_recognizer
import text_generation
import wake_word_detection

import json
import random
import requests
from bs4 import BeautifulSoup

#-------------------------------------------------------------------------------------------------------------------------#

def playsound(filename):
    sound = AudioSegment.from_file(filename)
    play(sound)

def num_to_word(num):
    pass

def get_weather(city) -> str:
    url = f"https://rp5.ru/Погода_в_{city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature_div = soup.find('div', class_='t_0')
        if temperature_div:
            temperature = temperature_div.text.strip()
            return temperature
        else:
            return "Не удалось найти информацию о погоде."
    return "Не удалось получить данные о погоде." 

def dialoque(question_voice: str):
    messages = []
    question = question_voice
    messages.append({"role": "user", "content": question})

    answer = text_generation.ask_gpt(messages=messages)
    messages.append({"role": "assistant", "content": answer})
    
#-------------------------------------------------------------------------------------------------------------------------#

with open(r'py_scripts/voice_answers.json') as answers_file:
    answers = json.load(answers_file)

def main():
    AImode = False
    WeatherMode = False
    WikiMode = False

    if wake_word_detection.wake_word_detection(access_key="access_key", keyword_paths=[r"keyword_paths"], keywords=["hey sasha"]):
        playsound(random.choice(answers['greeting']))

    while True:
        recognized_text = stt.listen()

        if cmd_recognizer.matching(recognized_text) not in config.VA_CMD:
            playsound(random.choice(answers['understanding']))
            continue


        elif cmd_recognizer.matching(recognized_text) == "speaking_with_ai":
            AImode = True
            playsound(random.choice(answers['agreement']))
            playsound(answers['request'][0])

            while AImode:
                text = stt.listen()
                if cmd_recognizer.matching(text) == "stop_speaking_with_ai":
                    playsound(random.choice(answers['agreement']))
                    AImode = False
                    break
                dialoque(text) 


        elif cmd_recognizer.matching(recognized_text) == "weather": #BETA
            playsound(answers['weather_report'][0])
            city = stt.listen()
            res = get_weather(city)
            if res.isalnum():
                ans = f"Температура в городе {city} {res} градусов цельсия"
                tts.va_speak(ans)
            else:
                tts.va_speak(res)

        elif cmd_recognizer.matching(recognized_text) == "stop_weather":
            pass


        elif cmd_recognizer.matching(recognized_text) == "wiki": #BETA
            WikiMode = True
            while WikiMode:
                playsound(answers['wiki'][3]) #назовите имя статьи

                title = stt.listen()
                if cmd_recognizer.matching(title) == 'stop_wiki':
                    playsound(random.choice(answers['agreement']))
                    WikiMode = False
                    break

                wiki_article = wiki.WikipediaArticle(language='ru')

                if not wiki_article.search_article(title):
                    playsound(answers['wiki'][2]) #статья не найдена
                    continue

                else:
                    playsound(answers['wiki'][1]) #вот содержание статьи
                    print("Содержание статьи:")

                    wiki_article.print_sections(sections=wiki_article.page.sections) #BUG

                    while WikiMode:
                        playsound(answers['wiki'][0]) #назовите имя раздела для получения содержания
                        user_input = stt.listen()

                        if cmd_recognizer.matching(user_input) == 'stop_wiki':
                            playsound(random.choice(answers['agreement']))
                            WikiMode = False
                            break

                        section = wiki_article.get_section_content(user_input)

                        if not section:
                            playsound(answers['wiki'][4]) #раздел не найден
                            print("Раздел не найден.")

                        else:
                            playsound(answers['wiki'][5]) #вот содержание раздела
                            print(f"\nСодержание раздела '{section.title}':\n") #BUG
                            print(section.text) #BUG
                            WikiMode = False
                            

if __name__ == '__main__':
    print(f'Ассистент {config.VA_NAME} {config.VA_VER} начал работу\n')
    print("Слушаю...\n")
    main()


