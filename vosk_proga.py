import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import asyncio
from tts import speak_word
from gpt_new import gpt
import threading


# Проверяем наличие модели
model_path = "model_vosk/vosk-model-small-ru-0.22"
messages = []
model = Model(model_path)  # Убедитесь, что путь к вашей модели правильный.
recognizer = KaldiRecognizer(model, 16000)

is_listening = False  # Переменная состояния, чтобы отслеживать, идет ли распознавание
timer = None


def set_listening_state(state):
    global is_listening
    is_listening = state
    print(is_listening)

def reset_timer():
    global timer
    # Если таймер уже существует, отменяем его
    if timer is not None:
        timer.cancel()


def start_timer():
    global timer
    # Если таймер уже существует, отменяем его
    if timer is not None:
        timer.cancel()

    # Запускаем новый таймер на 15 секунд
    timer = threading.Timer(15.0, stop_listening)
    timer.start()




def stop_listening():
    global is_listening
    is_listening = False  # Остановите распознавание
    print("Время истекло, распознавание остановлено.")

async def stt():
    global is_listening  # Указываем на использование глобальной переменной
    global messages

    print("Начинаю распознавание...")
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()
    print("Слушаю...")  # Уведомление о начале прослушивания
    print(is_listening)
    # Читаем данные и распознаем речь
    try:
        while is_listening:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                if text:
                    print(f"Распознанный текст: {text}")
                    print(messages)
                    reset_timer()
                    print('тайер сброшел')


                    messages = await gpt(messages= messages, new_message= text)  # Обработка распознанного текста
                    print('запуск таймера')
                    start_timer()


    except KeyboardInterrupt:
        print("Остановка распознавания...")

    finally:
        # Закрываем поток и освобождаем ресурсы
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Распознавание завершено.")