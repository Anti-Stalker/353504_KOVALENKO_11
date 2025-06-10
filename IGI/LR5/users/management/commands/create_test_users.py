from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает тестовых пользователей'

    def handle(self, *args, **options):
        # Создаем суперпользователя
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            phone='+79991111111',
            age=30,
            address='г. Москва, ул. Администраторская, д. 1'
        )

        # Создаем сотрудника
        staff_user = User.objects.create_user(
            username='staff_user',
            email='staff@example.com',
            password='staffpass123',
            role='staff',
            phone='+79992222222',
            age=25,
            address='г. Москва, ул. Пушкина, д. 1'
        )
        staff_user.is_staff = True
        staff_user.save()

        # Создаем обычного пользователя
        customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customerpass123',
            role='customer',
            phone='+79993333333',
            age=20,
            address='г. Санкт-Петербург, ул. Гоголя, д. 2'
        )

        self.stdout.write(self.style.SUCCESS('Тестовые пользователи успешно созданы')) 