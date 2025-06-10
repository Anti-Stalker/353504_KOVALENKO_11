import os
import django
from datetime import datetime, timedelta

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

from django.utils import timezone
from users.models import CustomUser

def restore_users():
    # Список пользователей для восстановления
    users_data = [
        {
            'username': 'auth',
            'password': '123123',
            'email': 'auth@example.com',
            'phone': '+375291111111',
            'is_staff': False,
            'is_superuser': False,
            'date_of_birth': timezone.now().date() - timedelta(days=25*365),  # 25 лет
        },
        {
            'username': 'auth2',
            'password': '123123',
            'email': 'auth2@example.com',
            'phone': '+375292222222',
            'is_staff': False,
            'is_superuser': False,
            'date_of_birth': timezone.now().date() - timedelta(days=30*365),  # 30 лет
        },
        {
            'username': 'auth3',
            'password': '123123',
            'email': 'auth3@example.com',
            'phone': '+375295555555',
            'is_staff': False,
            'is_superuser': False,
            'date_of_birth': timezone.now().date() - timedelta(days=27*365),  # 27 лет
        },
        {
            'username': 'staff',
            'password': '123123',
            'email': 'staff@example.com',
            'phone': '+375293333333',
            'is_staff': True,
            'is_superuser': False,
            'date_of_birth': timezone.now().date() - timedelta(days=35*365),  # 35 лет
        },
        {
            'username': 'superuser',
            'password': '123123',
            'email': 'admin@example.com',
            'phone': '+375294444444',
            'is_staff': True,
            'is_superuser': True,
            'date_of_birth': timezone.now().date() - timedelta(days=40*365),  # 40 лет
        }
    ]

    restored_users = []
    for user_data in users_data:
        username = user_data.pop('username')
        password = user_data.pop('password')
        
        # Удаляем существующего пользователя, если он есть
        CustomUser.objects.filter(username=username).delete()
        
        # Создаем нового пользователя
        user = CustomUser.objects.create_user(
            username=username,
            **user_data
        )
        user.set_password(password)
        user.save()
        
        restored_users.append(user)
        print(f"Восстановлен пользователь: {username}")
    
    return restored_users

if __name__ == "__main__":
    print("Начало восстановления пользователей...")
    users = restore_users()
    print(f"Восстановлено пользователей: {len(users)}")
    print("Восстановление завершено!") 