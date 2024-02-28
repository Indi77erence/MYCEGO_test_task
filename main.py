import asyncio
from io import BytesIO

import requests
from PIL import Image
import yadisk

from combined_image import combined
from config import TOKEN

url = "https://disk.yandex.ru/d/V47MEP5hZ3U1kg"
name_dir = ["1388_6_Наклейки 3-D_2"]


async def main():
	client = yadisk.AsyncClient(token=f"{TOKEN}")  # Экземпляр асинхронного клиента Яндекс.Диска
	async with client:  # Открываем асинхронное соединение с клиентом
		if await client.check_token():  # Проверяем, валиден ли токен
			if await client.public_exists(url):  # Проверяем, существует ли публичная директория по указанному URL
				items = await client.public_listdir(url)  # Получаем список элементов в публичной директории
				images = []  # Создаём пустой список для хранения изображений
				async for item in items:
					if item.name in name_dir:
						files = await item.public_listdir(path=item.path + '/')   # Получаем список файлов внутри данной директории
						async for file in files:
							response = requests.get(file.file)
							image = Image.open(BytesIO(response.content))  # Открываем изображение из байтового потока
							images.append(image)
	return await combined(images)  # Вызываем асинхронную функцию для объединения изображений и возврата результата

asyncio.run(main())
