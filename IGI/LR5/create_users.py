import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

from users.models import CustomUser
from django.contrib.auth.models import Group, Permission

# Удаляем всех существующих пользователей
CustomUser.objects.all().delete()

# Создаем базовую дату для возраста 20 лет
date_20_years = date.today() - timedelta(days=20*365)
# Создаем дату для возраста 14 лет
date_14_years = date.today() - timedelta(days=14*365)

# Создаем пользователей
users_data = [
    {
        'username': 'unauth',
        'password': '123123',
        'email': 'unauth@example.com',
        'phone': '+375290000000',
        'date_of_birth': date_20_years,
        'is_staff': False,
        'is_superuser': False,
        'is_active': True
    },
    {
        'username': 'auth',
        'password': '123123',
        'email': 'auth@example.com',
        'phone': '+375291111111',
        'date_of_birth': date_20_years,
        'is_staff': False,
        'is_superuser': False,
        'is_active': True
    },
    {
        'username': 'staff',
        'password': '123123',
        'email': 'staff@example.com',
        'phone': '+375292222222',
        'date_of_birth': date_20_years,
        'is_staff': True,
        'is_superuser': False,
        'is_active': True
    },
    {
        'username': 'superuser',
        'password': '123123',
        'email': 'superuser@example.com',
        'phone': '+375293333333',
        'date_of_birth': date_20_years,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True
    },
    {
        'username': 'auth2',
        'password': '123123',
        'email': 'auth2@example.com',
        'phone': '+375294444444',
        'date_of_birth': date_14_years,
        'is_staff': False,
        'is_superuser': False,
        'is_active': True
    }
]

# Создаем пользователей
for user_data in users_data:
    user = CustomUser.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        phone=user_data['phone'],
        date_of_birth=user_data['date_of_birth'],
        is_staff=user_data['is_staff'],
        is_superuser=user_data['is_superuser'],
        is_active=user_data['is_active']
    )
    print(f"Created user: {user.username}")

print("\nAll users have been created successfully!") 