from django.core.management.base import BaseCommand
from django.core.files import File
from content.models import Employee, Article
from django.conf import settings
import os
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with test content'

    def handle(self, *args, **kwargs):
        # Удаляем существующих сотрудников
        Employee.objects.all().delete()

        # Создаем тестовых сотрудников
        employees_data = [
            {
                'name': 'Иванов Иван Иванович',
                'position': 'Генеральный директор',
                'description': 'Руководит компанией с момента основания. Отвечает за стратегическое развитие и общее управление.',
                'age': 45,
                'experience': 20,
                'email': 'ivanov@bookstore.com',
                'phone': '+375 (29) 111-11-11'
            },
            {
                'name': 'Петрова Анна Сергеевна',
                'position': 'Главный бухгалтер',
                'description': 'Ведет финансовый учет и отчетность. Опытный специалист в области финансов.',
                'age': 38,
                'experience': 15,
                'email': 'petrova@bookstore.com',
                'phone': '+375 (29) 222-22-22'
            },
            {
                'name': 'Сидоров Петр Николаевич',
                'position': 'Заведующий отделом художественной литературы',
                'description': 'Эксперт по современной и классической литературе. Формирует ассортимент художественной литературы.',
                'age': 35,
                'experience': 12,
                'email': 'sidorov@bookstore.com',
                'phone': '+375 (29) 333-33-33'
            },
            {
                'name': 'Козлова Мария Александровна',
                'position': 'HR-менеджер',
                'description': 'Отвечает за подбор и развитие персонала. Организует корпоративные мероприятия.',
                'age': 29,
                'experience': 7,
                'email': 'kozlova@bookstore.com',
                'phone': '+375 (29) 444-44-44'
            },
            {
                'name': 'Новиков Дмитрий Игоревич',
                'position': 'IT-специалист',
                'description': 'Обеспечивает работу информационных систем и сайта магазина.',
                'age': 31,
                'experience': 8,
                'email': 'novikov@bookstore.com',
                'phone': '+375 (29) 555-55-55'
            },
            {
                'name': 'Морозова Екатерина Павловна',
                'position': 'Маркетолог',
                'description': 'Разрабатывает и реализует маркетинговую стратегию. Ведет социальные сети.',
                'age': 27,
                'experience': 5,
                'email': 'morozova@bookstore.com',
                'phone': '+375 (29) 666-66-66'
            },
            {
                'name': 'Волков Андрей Владимирович',
                'position': 'Заведующий отделом научной литературы',
                'description': 'Специализируется на научной и технической литературе. Консультирует по профессиональной литературе.',
                'age': 33,
                'experience': 10,
                'email': 'volkov@bookstore.com',
                'phone': '+375 (29) 777-77-77'
            },
            {
                'name': 'Соколова Ольга Дмитриевна',
                'position': 'Старший кассир',
                'description': 'Координирует работу кассового узла. Обучает новых сотрудников.',
                'age': 36,
                'experience': 14,
                'email': 'sokolova@bookstore.com',
                'phone': '+375 (29) 888-88-88'
            },
            {
                'name': 'Попов Сергей Александрович',
                'position': 'Заведующий складом',
                'description': 'Управляет складским хозяйством. Организует прием и отгрузку товара.',
                'age': 42,
                'experience': 16,
                'email': 'popov@bookstore.com',
                'phone': '+375 (29) 999-99-99'
            },
            {
                'name': 'Лебедева Наталья Игоревна',
                'position': 'Специалист по работе с клиентами',
                'description': 'Работает с клиентами, обрабатывает заказы и консультирует по ассортименту.',
                'age': 25,
                'experience': 3,
                'email': 'lebedeva@bookstore.com',
                'phone': '+375 (29) 000-00-00'
            }
        ]

        # Создаем сотрудников
        for data in employees_data:
            employee = Employee.objects.create(**data)
            # Добавляем фото по умолчанию
            default_photo_path = os.path.join('media/employees', 'default.png')
            if os.path.exists(default_photo_path):
                with open(default_photo_path, 'rb') as f:
                    employee.photo.save('employee.png', File(f), save=True)

        # Удаляем существующие новости
        Article.objects.all().delete()

        # Создаем новости
        articles_data = [
            {
                'title': 'Новинки литературы',
                'short_description': 'Обзор самых интересных книжных новинок этого месяца',
                'content': 'Подробный обзор новых поступлений в наш магазин...',
                'is_published': True
            },
            {
                'title': 'Как выбрать книгу',
                'short_description': 'Советы по выбору книг для разных возрастов и интересов',
                'content': 'Полезные рекомендации по выбору литературы...',
                'is_published': True
            },
            {
                'title': 'Топ-10 книг месяца',
                'short_description': 'Самые популярные книги по версии наших читателей',
                'content': 'Рейтинг самых популярных книг этого месяца...',
                'is_published': True
            },
            {
                'title': 'Интервью с автором',
                'short_description': 'Эксклюзивное интервью с известным писателем',
                'content': 'Интересная беседа о литературе и творчестве...',
                'is_published': True
            },
            {
                'title': 'Книжные тренды',
                'short_description': 'Актуальные тренды в мире литературы',
                'content': 'Анализ современных тенденций в литературе...',
                'is_published': True
            }
        ]

        # Создаем новости и добавляем изображения
        for article_data in articles_data:
            article = Article.objects.create(**article_data)
            # Добавляем изображение по умолчанию
            article.save()  # Это автоматически добавит default.png из настроек модели

        self.stdout.write(self.style.SUCCESS('Successfully populated articles'))