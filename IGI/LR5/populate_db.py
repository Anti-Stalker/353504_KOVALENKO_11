import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStore.settings')
django.setup()

from django.utils import timezone
from books.models import Author, Genre, Language, UnitOfMeasure, Book
from content.models import Article, CompanyInfo, Term, Employee, Vacancy
from users.models import CustomUser

def create_users():
    # Создаем 10 пользователей
    users = []
    for i in range(1, 11):
        username = f'user{i}'
        if not CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.create_user(
                username=username,
                password='123123',
                email=f'user{i}@example.com',
                phone=f'+37529{random.randint(1000000, 9999999)}',
                date_of_birth=timezone.now().date() - timedelta(days=random.randint(6570, 25550))  # От 18 до 70 лет
            )
            users.append(user)
    return users

def create_authors():
    # Создаем 10 авторов
    authors = []
    names = [
        "Александр Пушкин", "Лев Толстой", "Федор Достоевский", "Николай Гоголь",
        "Михаил Булгаков", "Антон Чехов", "Иван Тургенев", "Сергей Есенин",
        "Марина Цветаева", "Анна Ахматова"
    ]
    for name in names:
        if not Author.objects.filter(name=name).exists():
            author = Author.objects.create(
                name=name,
                date_of_birth=timezone.now().date() - timedelta(days=random.randint(25550, 40000))
            )
            authors.append(author)
    return authors

def create_genres():
    # Создаем жанры
    genres = []
    genre_names = [
        "Роман", "Поэзия", "Фантастика", "Детектив", "Приключения",
        "Научная литература", "Историческая проза", "Драма", "Комедия", "Триллер"
    ]
    for name in genre_names:
        if not Genre.objects.filter(name=name).exists():
            genre = Genre.objects.create(name=name)
            genres.append(genre)
    return genres

def create_languages():
    # Создаем языки
    languages = []
    language_names = ["Русский", "Английский", "Французский", "Немецкий", "Испанский",
                     "Итальянский", "Китайский", "Японский", "Польский", "Белорусский"]
    for name in language_names:
        if not Language.objects.filter(name=name).exists():
            language = Language.objects.create(name=name)
            languages.append(language)
    return languages

def create_units():
    # Создаем единицы измерения
    units = []
    unit_data = [
        ("Штука", "шт."),
        ("Комплект", "компл."),
        ("Набор", "наб."),
        ("Упаковка", "уп."),
        ("Коробка", "кор."),
        ("Пачка", "пач."),
        ("Том", "том"),
        ("Экземпляр", "экз."),
        ("Серия", "сер."),
        ("Издание", "изд.")
    ]
    for name, short_name in unit_data:
        if not UnitOfMeasure.objects.filter(name=name).exists():
            unit = UnitOfMeasure.objects.create(name=name, short_name=short_name)
            units.append(unit)
    return units

def create_books(authors, genres, languages, units):
    # Создаем 10 книг
    books = []
    titles = [
        "Война и мир", "Преступление и наказание", "Мастер и Маргарита",
        "Евгений Онегин", "Мертвые души", "Отцы и дети", "Анна Каренина",
        "Вишневый сад", "Идиот", "Герой нашего времени"
    ]
    for title in titles:
        if not Book.objects.filter(title=title).exists():
            book = Book.objects.create(
                title=title,
                summary=f"Краткое содержание книги {title}",
                imprint=random.choice(["Эксмо", "АСТ", "Питер", "Росмэн", "Альпина"]),
                ISBN=f"978-3-16-{random.randint(100000, 999999)}-0",
                language=random.choice(languages),
                age_restriction=random.choice([0, 6, 12, 16, 18]),
                price=Decimal(str(random.uniform(10.0, 100.0))).quantize(Decimal('0.01')),
                quantity=random.randint(1, 100),
                unit=random.choice(units)
            )
            # Выбираем случайное количество авторов, но не больше, чем есть в списке
            num_authors = min(random.randint(1, 3), len(authors))
            book.author.set(random.sample(authors, num_authors))
            
            # Выбираем случайное количество жанров, но не больше, чем есть в списке
            num_genres = min(random.randint(1, 3), len(genres))
            book.genre.set(random.sample(genres, num_genres))
            
            books.append(book)
    return books

def create_articles():
    # Создаем 10 статей
    articles = []
    titles = [
        "Новинки литературы", "Как выбрать книгу", "Топ-10 книг месяца",
        "Интервью с автором", "Книжные тренды", "История книгопечатания",
        "Электронные книги vs бумажные", "Как привить любовь к чтению",
        "Книжные ярмарки 2024", "Будущее книжной индустрии"
    ]
    for title in titles:
        if not Article.objects.filter(title=title).exists():
            article = Article.objects.create(
                title=title,
                short_description=f"Краткое описание статьи {title}",
                content=f"Полное содержание статьи {title}...",
                is_published=True
            )
            articles.append(article)
    return articles

def create_company_info():
    # Создаем информацию о компании
    if not CompanyInfo.objects.exists():
        company = CompanyInfo.objects.create(
            name="Книжный магазин 'Читай-город'",
            description="Лучший книжный магазин в городе",
            history="История нашего магазина началась в 2020 году...",
            requisites="ИНН: 1234567890\nКПП: 123456789\nОГРН: 1234567890123"
        )
        return [company]
    return []

def create_terms():
    # Создаем 10 терминов
    terms = []
    qa_pairs = [
        ("Что такое ISBN?", "ISBN - это уникальный номер книжного издания..."),
        ("Как оформить возврат?", "Для возврата товара необходимо..."),
        ("Какие способы оплаты?", "Мы принимаем наличные, карты и онлайн-платежи..."),
        ("Условия доставки", "Доставка осуществляется по всей стране..."),
        ("Программа лояльности", "Наша программа лояльности предусматривает..."),
        ("Подарочные сертификаты", "Вы можете приобрести подарочный сертификат..."),
        ("Предзаказ книг", "Предзаказ позволяет зарезервировать книгу..."),
        ("Условия хранения", "Мы храним книги в специальных условиях..."),
        ("Гарантия качества", "Мы гарантируем качество всех наших товаров..."),
        ("Бонусная программа", "Участвуйте в нашей бонусной программе...")
    ]
    for question, answer in qa_pairs:
        if not Term.objects.filter(question=question).exists():
            term = Term.objects.create(question=question, answer=answer)
            terms.append(term)
    return terms

def create_employees():
    # Создаем 10 сотрудников
    employees = []
    employee_data = [
        ("Иванов Иван", "Директор"),
        ("Петрова Мария", "Менеджер по продажам"),
        ("Сидоров Алексей", "Консультант"),
        ("Козлова Анна", "Бухгалтер"),
        ("Морозов Дмитрий", "Администратор"),
        ("Васильева Елена", "HR-менеджер"),
        ("Николаев Сергей", "Маркетолог"),
        ("Смирнова Ольга", "Кассир"),
        ("Кузнецов Андрей", "Кладовщик"),
        ("Попова Татьяна", "Менеджер по закупкам")
    ]
    for name, position in employee_data:
        if not Employee.objects.filter(name=name).exists():
            employee = Employee.objects.create(
                name=name,
                position=position,
                description=f"Описание обязанностей {position}",
                phone=f"+37529{random.randint(1000000, 9999999)}",
                email=f"{name.split()[1].lower()}@bookstore.com"
            )
            employees.append(employee)
    return employees

def create_vacancies():
    # Создаем 10 вакансий
    vacancies = []
    vacancy_data = [
        ("Продавец-консультант", 800, 1200),
        ("Кассир", 700, 1000),
        ("Менеджер по продажам", 1200, 2000),
        ("Кладовщик", 800, 1100),
        ("Администратор", 900, 1500),
        ("Маркетолог", 1500, 2500),
        ("HR-специалист", 1200, 2000),
        ("Бухгалтер", 1300, 2200),
        ("Курьер", 600, 900),
        ("SMM-менеджер", 1000, 1800)
    ]
    for title, salary_from, salary_to in vacancy_data:
        if not Vacancy.objects.filter(title=title).exists():
            vacancy = Vacancy.objects.create(
                title=title,
                description=f"Описание вакансии {title}",
                requirements=f"Требования к вакансии {title}",
                salary_from=salary_from,
                salary_to=salary_to,
                is_active=True
            )
            vacancies.append(vacancy)
    return vacancies

def main():
    print("Начало заполнения базы данных...")
    
    users = create_users()
    print(f"Создано пользователей: {len(users)}")
    
    authors = create_authors()
    print(f"Создано авторов: {len(authors)}")
    
    genres = create_genres()
    print(f"Создано жанров: {len(genres)}")
    
    languages = create_languages()
    print(f"Создано языков: {len(languages)}")
    
    units = create_units()
    print(f"Создано единиц измерения: {len(units)}")
    
    books = create_books(authors, genres, languages, units)
    print(f"Создано книг: {len(books)}")
    
    articles = create_articles()
    print(f"Создано статей: {len(articles)}")
    
    company_info = create_company_info()
    print(f"Создано записей о компании: {len(company_info)}")
    
    terms = create_terms()
    print(f"Создано терминов: {len(terms)}")
    
    employees = create_employees()
    print(f"Создано сотрудников: {len(employees)}")
    
    vacancies = create_vacancies()
    print(f"Создано вакансий: {len(vacancies)}")
    
    print("База данных успешно заполнена!")

if __name__ == "__main__":
    main() 