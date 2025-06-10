import os
import django
import random
from datetime import timedelta

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

from django.utils import timezone
from books.models import Book, PurchaseHistory
from users.models import CustomUser

def create_purchase_history():
    # Получаем всех пользователей и книги
    users = CustomUser.objects.all()
    books = Book.objects.all()
    
    if not users or not books:
        print("Нет пользователей или книг в базе данных!")
        return []

    purchases = []
    # Создаем историю покупок за последние 30 дней
    for user in users:
        # Каждый пользователь сделает от 1 до 5 покупок
        num_purchases = random.randint(1, 5)
        for _ in range(num_purchases):
            # Выбираем случайную книгу
            book = random.choice(books)
            # Выбираем случайное количество книг (1-3)
            quantity = random.randint(1, 3)
            # Выбираем случайную дату за последние 30 дней
            created_at = timezone.now() - timedelta(days=random.randint(0, 30))
            
            # Создаем запись о покупке
            purchase = PurchaseHistory.objects.create(
                user=user,
                book=book,
                quantity=quantity,
                created_at=created_at,
                total_price=book.price * quantity,
                delivery_method=random.choice(['pickup', 'delivery'])
            )
            purchases.append(purchase)
            print(f"Создана покупка: {user.username} купил {book.title} ({quantity} шт.)")

    return purchases

if __name__ == "__main__":
    print("Начало создания истории покупок...")
    purchases = create_purchase_history()
    print(f"Создано записей о покупках: {len(purchases)}")
    print("Создание истории покупок завершено!") 