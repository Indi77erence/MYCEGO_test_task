from io import BytesIO

from PIL import Image

tiff_filename = "Result.tiff"

padding_right = 20  # Отступы между фотографиями в одном ряду
padding_bottom = 20  # Отступы между рядами
background_color = (255, 255, 255) # фон изображения


async def combined(images: list[Image.Image]) -> Image.Image:
    num_images = len(images)
    if num_images > 0:
        # Количество строк для расположения изображений в ряд
        num_rows = (num_images + 3) // 4

        # Вычисляем ширину объединенного изображения с учётом отступов между изображениями
        combined_image_width = images[0].width * min(num_images, 4) + padding_right * (min(num_images, 4) - 1)

        # Вычисляем высоту объединенного изображения
        combined_image_height = images[0].height * num_rows + padding_bottom * (num_rows - 1)

        # Создаём новое изображение с заданными размерами и белым фоном
        combined_image = Image.new("RGB", (combined_image_width, combined_image_height), background_color)

        # Объединяем изображения в одно
        for i in range(num_images):
            x_offset = (i % 4) * (images[i].width + padding_right)
            y_offset = (i // 4) * (images[i].height + padding_bottom)
            combined_image.paste(images[i], (x_offset, y_offset))

        # Создаём объект BytesIO для временного хранения изображения в формате TIFF
        tiff_bytes = BytesIO()
        combined_image.save(tiff_bytes, format="TIFF")

        with open(tiff_filename, "wb") as f:
            f.write(tiff_bytes.getvalue())

        print(f"Создан файл: {tiff_filename}")
    else:
        print("Нет фотографий для объединения")
