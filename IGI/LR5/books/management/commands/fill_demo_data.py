from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Book, Author, Genre, Language, BookInstance
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных демонстрационными данными'

    def handle(self, *args, **options):
        # Создаем языки
        languages = [
            Language.objects.create(name='Русский'),
            Language.objects.create(name='Английский'),
            Language.objects.create(name='Французский'),
        ]

        # Создаем жанры
        genres = [
            Genre.objects.create(name='Роман'),
            Genre.objects.create(name='Фантастика'),
            Genre.objects.create(name='Детектив'),
            Genre.objects.create(name='Поэзия'),
            Genre.objects.create(name='Научная литература'),
        ]

        # Создаем авторов
        authors = [
            Author.objects.create(
                name='Александр Пушкин',
                date_of_birth='1799-06-06',
                date_of_death='1837-02-10'
            ),
            Author.objects.create(
                name='Лев Толстой',
                date_of_birth='1828-09-09',
                date_of_death='1910-11-20'
            ),
            Author.objects.create(
                name='Федор Достоевский',
                date_of_birth='1821-11-11',
                date_of_death='1881-02-09'
            ),
            Author.objects.create(
                name='Агата Кристи',
                date_of_birth='1890-09-15',
                date_of_death='1976-01-12'
            ),
            Author.objects.create(
                name='Жюль Верн',
                date_of_birth='1828-02-08',
                date_of_death='1905-03-24'
            ),
        ]

        # Создаем книги
        books_data = [
            {
                'title': 'Евгений Онегин',
                'summary': 'Роман в стихах о любви и судьбе',
                'isbn': '9785699123456',
                'author': [authors[0]],
                'genre': [genres[0], genres[3]],
                'language': languages[0]
            },
            {
                'title': 'Война и мир',
                'summary': 'Эпопея о войне 1812 года',
                'isbn': '9785699123457',
                'author': [authors[1]],
                'genre': [genres[0]],
                'language': languages[0]
            },
            {
                'title': 'Преступление и наказание',
                'summary': 'Психологический роман о преступлении',
                'isbn': '9785699123458',
                'author': [authors[2]],
                'genre': [genres[0]],
                'language': languages[0]
            },
            {
                'title': 'Десять негритят',
                'summary': 'Детективный роман об убийствах на острове',
                'isbn': '9785699123459',
                'author': [authors[3]],
                'genre': [genres[2]],
                'language': languages[1]
            },
            {
                'title': '20000 лье под водой',
                'summary': 'Приключения капитана Немо',
                'isbn': '9785699123460',
                'author': [authors[4]],
                'genre': [genres[1]],
                'language': languages[2]
            },
            {
                'title': 'Капитанская дочка',
                'summary': 'Исторический роман о восстании Пугачева',
                'isbn': '9785699123461',
                'author': [authors[0]],
                'genre': [genres[0]],
                'language': languages[0]
            },
            {
                'title': 'Анна Каренина',
                'summary': 'Роман о трагической любви',
                'isbn': '9785699123462',
                'author': [authors[1]],
                'genre': [genres[0]],
                'language': languages[0]
            },
            {
                'title': 'Идиот',
                'summary': 'Роман о князе Мышкине',
                'isbn': '9785699123463',
                'author': [authors[2]],
                'genre': [genres[0]],
                'language': languages[0]
            },
            {
                'title': 'Убийство в Восточном экспрессе',
                'summary': 'Детектив в поезде',
                'isbn': '9785699123464',
                'author': [authors[3]],
                'genre': [genres[2]],
                'language': languages[1]
            },
            {
                'title': 'Таинственный остров',
                'summary': 'Приключения на необитаемом острове',
                'isbn': '9785699123465',
                'author': [authors[4]],
                'genre': [genres[1]],
                'language': languages[2]
            },
        ]

        for book_data in books_data:
            book = Book.objects.create(
                title=book_data['title'],
                summary=book_data['summary'],
                ISBN=book_data['isbn'],
                language=book_data['language'],
                imprint='Издательство "Классика"'
            )
            book.author.set(book_data['author'])
            book.genre.set(book_data['genre'])

            # Создаем экземпляры для каждой книги
            for _ in range(random.randint(1, 3)):
                status = random.choice(['m', 'o', 'a', 'r'])
                due_back = datetime.now().date() + timedelta(days=random.randint(1, 30)) if status == 'o' else None
                BookInstance.objects.create(
                    book=book,
                    uniqueId=f"{book.ISBN}-{_}",
                    status=status,
                    due_back=due_back
                )

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные успешно созданы')) 