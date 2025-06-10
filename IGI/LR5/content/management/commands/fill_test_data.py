from django.core.management.base import BaseCommand
from django.utils import timezone
from content.models import Article, CompanyInfo, Dictionary, Employee, Vacancy, Review, Promo
from datetime import timedelta

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        # Создаем статью
        Article.objects.create(
            title="Новинки литературы этой весной",
            content="Подробное описание новых книг, которые появились в нашем магазине этой весной...",
            short_description="Обзор новых поступлений в нашем магазине",
        )

        # Создаем информацию о компании
        CompanyInfo.objects.create(
            text="Наш книжный магазин работает с 2010 года...",
            video_url="https://example.com/video",
            history="2010 - Основание компании\n2015 - Открытие филиала\n2020 - Запуск онлайн-магазина",
            requisites="ИНН: 1234567890\nКПП: 123456789\nОГРН: 1234567890123"
        )

        # Создаем термины в словаре
        Dictionary.objects.create(
            question="Что такое ISBN?",
            answer="ISBN (International Standard Book Number) - это уникальный номер книжного издания..."
        )
        Dictionary.objects.create(
            question="Что такое твердый переплет?",
            answer="Твердый переплет - это тип обложки книги..."
        )

        # Создаем сотрудников
        Employee.objects.create(
            name="Иванов Иван Иванович",
            position="Главный менеджер",
            description="Управление магазином и работа с клиентами",
            phone="+7 (999) 123-45-67",
            email="ivanov@example.com"
        )
        Employee.objects.create(
            name="Петрова Мария Сергеевна",
            position="Консультант",
            description="Помощь в выборе книг, консультации по новинкам",
            phone="+7 (999) 765-43-21",
            email="petrova@example.com"
        )

        # Создаем вакансии
        Vacancy.objects.create(
            title="Продавец-консультант",
            description="Работа с клиентами в торговом зале",
            requirements="Знание современной литературы, опыт работы от 1 года",
            salary="от 40 000 руб.",
            is_active=True
        )
        Vacancy.objects.create(
            title="Менеджер по закупкам",
            description="Работа с поставщиками книжной продукции",
            requirements="Опыт работы в книжном бизнесе от 2 лет",
            salary="от 60 000 руб.",
            is_active=True
        )

        # Создаем отзывы
        Review.objects.create(
            name="Александр",
            rating=5,
            text="Отличный магазин! Большой выбор книг и приятные цены",
            is_published=True
        )
        Review.objects.create(
            name="Елена",
            rating=4,
            text="Хороший магазин, но хотелось бы больше новинок",
            is_published=True
        )

        # Создаем промокоды
        now = timezone.now()
        Promo.objects.create(
            code="SPRING2024",
            description="Весенняя скидка на все книги",
            discount=15.00,
            valid_from=now,
            valid_to=now + timedelta(days=30),
            is_active=True
        )
        Promo.objects.create(
            code="WELCOME",
            description="Скидка для новых клиентов",
            discount=10.00,
            valid_from=now,
            valid_to=now + timedelta(days=365),
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы')) 