import pyaudio
import pvporcupine
import struct
import asyncio
import os
from dotenv import load_dotenv
from tts import speak_word
from vosk_proga import set_listening_state, stt

load_dotenv()
access_key = os.getenv('ACCESS_KEY')


# Инициализация переменных состояния
is_running = False
is_listening = False  # Переменная состояния, чтобы отслеживать, идет ли распознавание


async def main():
    global is_running
    global is_listening  # Указываем на использование глобальной переменной
    porcupine = None
    pa = None
    audio_stream = None
    await speak_word('Готов к работе')
    print('ddddd')
    try:
        porcupine = pvporcupine.create(access_key=access_key, keywords=['computer'])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)

        while is_running:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0 and not is_listening:  # Проверяем, не ведется ли уже распознавание
                print('слово')
                await speak_word('слушаю')
                set_listening_state(True)

                # Запускаем функцию распознавания в отдельном потоке
                # await asyncio.to_thread(stt)  # Запускаем stt в отдельном потоке
                await stt()
                print("Вернуться в режим ожидания...")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        is_running = False


async def button_clicked():
    global is_running
    if not is_running:
        is_running = True
        await main()  # Запускаем main() асинхронно
    else:
        is_running = False
        print("Остановлено.")


