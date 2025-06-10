from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import Book, Author, Genre
from users.models import CustomUser
from analytics.models import Sale
from decimal import Decimal
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates test data for the bookstore'

    def handle(self, *args, **kwargs):
        # Создаем жанры
        genres = [
            'Фантастика', 'Детектив', 'Роман', 'Поэзия', 'Научная литература',
            'Детская литература', 'Бизнес', 'Психология', 'История', 'Философия'
        ]
        
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects.append(genre)
            if created:
                self.stdout.write(f'Created genre: {genre_name}')
        
        # Создаем авторов
        authors = [
            'Александр Пушкин', 'Лев Толстой', 'Федор Достоевский',
            'Николай Гоголь', 'Антон Чехов', 'Михаил Булгаков',
            'Иван Тургенев', 'Борис Пастернак', 'Анна Ахматова'
        ]
        
        author_objects = []
        for author_name in authors:
            author, created = Author.objects.get_or_create(name=author_name)
            author_objects.append(author)
            if created:
                self.stdout.write(f'Created author: {author_name}')
        
        # Создаем книги
        books = [
            'Евгений Онегин', 'Война и мир', 'Преступление и наказание',
            'Мертвые души', 'Вишневый сад', 'Мастер и Маргарита',
            'Отцы и дети', 'Доктор Живаго', 'Реквием'
        ]
        
        book_objects = []
        for i, title in enumerate(books):
            book = Book.objects.create(
                title=title,
                str_repr=title
            )
            book.author.add(author_objects[i])
            book.genre.add(random.choice(genre_objects))
            book_objects.append(book)
            self.stdout.write(f'Created book: {title}')
        
        # Создаем тестовых пользователей
        for i in range(10):
            username = f'user{i}'
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'user{i}@example.com',
                    'age': random.randint(18, 70),
                    'phone': f'+7900{random.randint(1000000, 9999999)}',
                    'role': 'customer'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {username}')
        
        # Создаем продажи
        customers = CustomUser.objects.filter(role='customer')
        now = timezone.now()
        
        for _ in range(50):
            sale_date = now - timedelta(days=random.randint(0, 30))
            book = random.choice(book_objects)
            customer = random.choice(customers)
            quantity = random.randint(1, 5)
            price = Decimal(random.uniform(500, 2000)).quantize(Decimal('0.01'))
            
            sale = Sale.objects.create(
                book=book,
                customer=customer,
                quantity=quantity,
                price=price,
                total=price * quantity,
                created_at=sale_date
            )
            self.stdout.write(f'Created sale: {sale}') 