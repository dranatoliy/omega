import config
import asyncio
from pvpor import button_clicked

print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")

# async def main():
#     await button_clicked()  # Предполагаем, что button_clicked() теперь асинхронная функция

if __name__ == "__main__":
    asyncio.run(button_clicked())
