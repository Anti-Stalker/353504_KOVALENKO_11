from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os

class Command(BaseCommand):
    help = 'Create test images for employees and news'

    def create_gradient_image(self, size, start_color, end_color, text):
        # Создаем новое изображение
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)

        # Создаем градиент
        for y in range(size[1]):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * y / size[1])
            g = int(start_color[1] + (end_color[1] - start_color[1]) * y / size[1])
            b = int(start_color[2] + (end_color[2] - start_color[2]) * y / size[1])
            draw.line([(0, y), (size[0], y)], fill=(r, g, b))

        # Добавляем текст
        text_color = (255, 255, 255)
        text_position = (size[0]//2, size[1]//2)
        draw.text(text_position, text, fill=text_color, anchor="mm")

        return image

    def handle(self, *args, **kwargs):
        # Создаем изображение для сотрудников
        employee_size = (300, 300)
        employee_start_color = (41, 128, 185)  # Синий
        employee_end_color = (52, 152, 219)    # Светло-синий
        employee_image = self.create_gradient_image(
            employee_size,
            employee_start_color,
            employee_end_color,
            "Employee\nPhoto"
        )

        # Создаем изображение для новостей
        news_size = (800, 400)
        news_start_color = (52, 73, 94)   # Темно-серый
        news_end_color = (44, 62, 80)     # Серый
        news_image = self.create_gradient_image(
            news_size,
            news_start_color,
            news_end_color,
            "News Image"
        )

        # Сохраняем изображения
        os.makedirs('media/employees', exist_ok=True)
        os.makedirs('media/articles', exist_ok=True)

        employee_image.save('media/employees/default.png')
        news_image.save('media/articles/default.png')

        self.stdout.write(self.style.SUCCESS('Successfully created test images')) 