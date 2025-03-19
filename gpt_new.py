from openai import AsyncOpenAI
import asyncio
import time
from tts import speak_word
import json
import os
from dotenv import load_dotenv
import tiktoken
import requests


encoding = tiktoken.encoding_for_model("gpt-4o-mini")  # Или другую модель, которую вы используете

load_dotenv()

PASS_GPT = os.getenv('PASS_GPT')

max_tokens = 40000

def auth():
    data = {
        "username": "a.drozdov@tcsbank.ru",
        "password": PASS_GPT
    }

    response = requests.post('https://openai-proxy.tcsbank.ru/auth/v1/token', json=data)

    access_token = response.json()['access_token']
    return access_token

def count_tokens(messages):
    tokens = 0
    for message in messages:
        tokens += len(encoding.encode(message['content'])) + 4  # +4 для роли сообщения и маркеров
    return tokens

def trim_messages_to_limit(messages, max_tokens):
    while count_tokens(messages) > max_tokens:
        # Удаляем самое старое сообщение
        messages.pop(0)
    return messages


client = AsyncOpenAI(api_key=auth(), base_url="https://openai-proxy.tcsbank.ru/public/v1")

async def gpt(messages, new_message):
    messages.append({"role": "user", "content": new_message})
    print(messages)
    # Удаляем старые сообщения если количество токенов превышает лимит
    trim_messages_to_limit(messages, max_tokens)
    stream = await client.chat.completions.create(
        messages=messages,
        stream=True,
        model="gpt-4o-mini",
        max_tokens=1000,
        temperature=1.0,
        extra_headers={
          'Accept': 'text/event-stream'
        }
    )
    assistant_reply = ""
    buffer = ""  # Буфер для накопления текста

    async for chunk in stream:
        if getattr(chunk, 'choices', None) and len(chunk.choices) > 0:
            delta = getattr(chunk.choices[0], 'delta', None)
            if delta is not None:
                content = getattr(delta, 'content', '')
                buffer += content  # Накопление текста в буфер

                # Проверяем, есть ли конец предложения
                if any(buffer.endswith(end) for end in '.!?'):
                    buffer = buffer.strip()  # Убираем лишние пробелы

                    if buffer:  # Проверяем, что буфер не пустой
                        print(f"Говорим: {buffer}")  # Отладочное сообщение
                        await speak_word(buffer)  # Озвучиваем полное предложение
                        assistant_reply +=buffer
                        buffer = ""  # Очищаем буфер для следующего предложения
            else:
                print("<delta отсутствует>", end='', flush=True)
        else:
            print("<choices отсутствуют>", end='', flush=True)

            # Если после завершения потока остались данные в буфере
    if buffer.strip():
        buffer = buffer.strip()  # Убираем лишние пробелы
        print(f"Говорим в конце: {buffer}")  # Отладочное сообщение
        await speak(buffer)  # Озвучиваем оставшееся содержимое
        assistant_reply += buffer
    messages.append({"role": "assistant", "content": assistant_reply})
    return messages

