import pygame
import tempfile
import asyncio
from gtts import gTTS
import collections
import os


async def speak_word(content: str):
    """Функция для озвучивания текста с использованием gTTS и Pygame."""
    print('начало')
    pygame.mixer.init()
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file_name = temp_file.name  # Получаем имя временного файла
        tts = gTTS(text=content, lang='ru')  # Укажите нужный язык
        tts.save(temp_file_name)  # Сохраняем аудиофайл в временный файл
        print('создали файл')
    try:
        # Воспроизводим аудиофайл с использованием Pygame
        pygame.mixer.music.load(temp_file_name)
        pygame.mixer.music.play()

        # Ждем завершения воспроизведения
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)  # Небольшая пауза, чтобы не загружать процессор
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    except PermissionError:
        print(f"Ошибка: Не удалось получить доступ к файлу: {temp_file_name}")
    finally:
        # Удаляем временный файл после завершения воспроизведения
        try:
            os.remove(temp_file_name)
        except PermissionError:
            print(f"Предупреждение: Не удалось удалить файл {temp_file_name}. Возможно, он еще занят.")
        except Exception as e:
            print(f"Произошла ошибка при удалении файла {temp_file_name}: {e}")

#
#
# # Инициализация
# pygame.mixer.init()
# audio_queue = collections.deque()
# is_playing = False
# play_event = asyncio.Event()
#
#
# async def play_next():
#     global is_playing
#     print('dsdsds')
#     while True:
#         # Ожидаем, пока не добавится файл в очередь
#         if not audio_queue:
#             await play_event.wait()  # Ждем, если очередь пуста
#             play_event.clear()  # Сбрасываем флаг
#
#         if audio_queue:
#             is_playing = True
#             file_path = audio_queue.popleft()  # Извлекаем следующий файл
#             print(f'Воспроизводим файл: {file_path}')
#
#             # Воспроизведение музыки
#             pygame.mixer.music.load(file_path)
#             pygame.mixer.music.play()
#
#             # Ждем завершения воспроизведения
#             while pygame.mixer.music.get_busy():
#                 await asyncio.sleep(0.1)  # Небольшая пауза
#
#             os.remove(file_path)  # Удаляем временный
#             print(f'Удалили файл: {file_path}')
#         else:
#             is_playing = False
#
# async def speak(content: str):
#     global is_playing
#
#     # Создаем временный файл
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
#         temp_file_name = temp_file.name  # Получаем имя временного файла
#         tts = gTTS(text=content, lang='ru')  # Укажите нужный язык
#         tts.save(temp_file_name)  # Сохраняем аудиофайл в временный файл
#         print('Создали файл:', temp_file_name)
#
#     # Добавляем файл в конец очереди
#     audio_queue.append(temp_file_name)
#
#     # Уведомляем о том, что в очередь добавлен новый файл
#     play_event.set()  # Устанавливаем событие, чтобы запустить воспроизведение