import config
from fuzzywuzzy import fuzz
import datetime
from tts import speak
import random
from num2words import num2words
import webbrowser
import subprocess



def va_respond(voice: str):
    print(voice)
    cmd = recognize_cmd(voice)

    if cmd['cmd'] not in config.VA_CMD_LIST.keys() or cmd['percent'] <=60:
        speak("Я тебя не понимаю?")
    else:
        execute_cmd(cmd['cmd'])


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        print(c,v)
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
            print(rc)

    print(rc)
    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «можно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']

        speak(random.choice(jokes))

    elif cmd == 'open_browser':
        # Укажем путь к Chrome
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        # Регистрируем браузер
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

        # Используем зарегистрированный браузер для открытия URL
        webbrowser.get('chrome').open("http://python.org")

    elif cmd == 'open_time':
        # Укажем путь к time
        process_time = subprocess.Popen([r"C:\Users\a.drozdov\AppData\Local\Programs\time-desktop\TiMe.exe"])

    elif cmd == 'kill_time':
        # Укажем путь к time
        process_name = "time.exe"
        subprocess.run(["taskkill", "/F", "/IM", process_name])
