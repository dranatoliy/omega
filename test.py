import pyaudio
import wave

# Параметры записи
FORMAT = pyaudio.paInt16  # Формат записи (16-бит)
CHANNELS = 2               # Количество каналов (1 - моно, 2 - стерео)
RATE = 44100               # Частота дискретизации (44.1 кГц)
CHUNK = 1024               # Размер буфера
RECORD_SECONDS = 5         # Время записи (в секундах)
WAVE_OUTPUT_FILENAME = "output.wav"  # Имя файла для сохранения

# Создаем объект PyAudio
p = pyaudio.PyAudio()

# Открываем поток для записи
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Запись Started...")

frames = []

# Запись аудио
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Запись Finished.")

# Останавливаем и закрываем поток
stream.stop_stream()
stream.close()
p.terminate()

# Сохраняем записанное аудио в WAV файл
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Записанный файл сохранён как {WAVE_OUTPUT_FILENAME}.")