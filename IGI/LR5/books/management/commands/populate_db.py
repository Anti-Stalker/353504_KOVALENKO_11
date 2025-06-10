from django.core.management.base import BaseCommand
from books.models import Book, Author, Genre, Language, UnitOfMeasure, PurchaseHistory
from content.models import Article, CompanyInfo, Term, Employee, Vacancy, Review, PromoCode
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Создаем суперпользователя для отзывов
        self.stdout.write('Creating test users...')
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            phone='+375 (29) 123-45-67',
            is_staff=True,
            is_superuser=True
        )
        test_user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test123',
            phone='+375 (29) 765-43-21'
        )

        # Создаем единицы измерения
        self.stdout.write('Creating units of measure...')
        unit = UnitOfMeasure.objects.create(
            name='Штука',
            short_name='шт.'
        )

        # Создаем языки
        self.stdout.write('Creating languages...')
        russian = Language.objects.create(name='Русский')
        english = Language.objects.create(name='English')

        # Создаем жанры
        self.stdout.write('Creating genres...')
        genres_data = [
            'Фантастика', 'Роман', 'Детектив', 'Поэзия', 'Драма',
            'Приключения', 'Историческая проза', 'Научная литература',
            'Психология', 'Философия'
        ]
        genres = [Genre.objects.create(name=name) for name in genres_data]

        # Создаем авторов
        self.stdout.write('Creating authors...')
        authors_data = [
            ('Александр', 'Пушкин', date(1799, 6, 6), date(1837, 2, 10)),
            ('Лев', 'Толстой', date(1828, 9, 9), date(1910, 11, 20)),
            ('Федор', 'Достоевский', date(1821, 11, 11), date(1881, 2, 9)),
            ('Николай', 'Гоголь', date(1809, 4, 1), date(1852, 3, 4)),
            ('Михаил', 'Булгаков', date(1891, 5, 15), date(1940, 3, 10)),
            ('Антон', 'Чехов', date(1860, 1, 29), date(1904, 7, 15)),
            ('Иван', 'Тургенев', date(1818, 11, 9), date(1883, 9, 3)),
            ('Михаил', 'Лермонтов', date(1814, 10, 15), date(1841, 7, 27)),
            ('Сергей', 'Есенин', date(1895, 10, 3), date(1925, 12, 28)),
            ('Борис', 'Пастернак', date(1890, 2, 10), date(1960, 5, 30))
        ]
        authors = []
        for first_name, last_name, birth_date, death_date in authors_data:
            author = Author.objects.create(
                name=f"{first_name} {last_name}",
                date_of_birth=birth_date,
                date_of_death=death_date
            )
            authors.append(author)

        # Создаем книги
        self.stdout.write('Creating books...')
        books_data = [
            {
                'title': 'Мастер и Маргарита',
                'summary': '''Величайший роман XX века, переведенный на множество языков и признанный классикой мировой литературы. 
                История о загадочном появлении в Москве Воланда и его свиты, о любви Мастера и Маргариты, о предательстве и верности, 
                о добре и зле. Роман-загадка, роман-притча, роман-откровение, в котором реальность переплетается с фантастикой, 
                а библейские мотивы - с сатирическим изображением советской действительности 1930-х годов. 
                Булгаков создал произведение, которое не перестает удивлять читателей своей многогранностью и глубиной смыслов.''',
                'price': Decimal('29.99'),
                'age_restriction': 16
            },
            {
                'title': 'Преступление и наказание',
                'summary': '''Один из самых значительных романов мировой литературы, в котором Достоевский поднимает вечные вопросы 
                о природе добра и зла, о границах человеческой свободы и ответственности за свои поступки. 
                История Родиона Раскольникова, бедного студента, решившегося на убийство старухи-процентщицы, 
                чтобы доказать себе и миру право сильной личности преступать моральные законы, 
                превращается в глубокое исследование человеческой души, ее способности к раскаянию и возрождению. 
                Роман, написанный в 1866 году, остается актуальным и сегодня, заставляя читателей задуматься 
                о последствиях своих действий и о цене, которую приходится платить за свои решения.''',
                'price': Decimal('24.99'),
                'age_restriction': 16
            },
            {
                'title': 'Война и мир',
                'summary': '''Монументальный роман-эпопея Льва Толстого, охватывающий период с 1805 по 1820 год. 
                На фоне исторических событий - войны с Наполеоном, пожара Москвы, партизанского движения - 
                разворачиваются судьбы главных героев: Андрея Болконского, Пьера Безухова, Наташи Ростовой и других. 
                Толстой мастерски переплетает исторические события с личными историями героев, 
                создавая многоплановое повествование о жизни, любви, войне, мире и поиске смысла существования. 
                Автор глубоко исследует характеры персонажей, показывая их развитие и изменение под влиянием 
                жизненных обстоятельств. Это не просто исторический роман, а философское размышление о судьбах 
                людей и народов, о роли личности в истории.''',
                'price': Decimal('34.99'),
                'age_restriction': 12
            },
            {
                'title': '1984',
                'summary': '''Культовый роман-антиутопия Джорджа Оруэлла, написанный в 1948 году. 
                Действие происходит в тоталитарном государстве Океания, где власть контролирует все аспекты 
                жизни граждан, включая их мысли. Главный герой, Уинстон Смит, работает в Министерстве Правды, 
                где занимается фальсификацией исторических документов. Он начинает сомневаться в системе и 
                вместе с возлюбленной Джулией пытается противостоять режиму. Роман поднимает важные вопросы 
                о свободе личности, манипуляции сознанием, тотальном контроле и человеческом достоинстве. 
                Многие термины из книги ("Большой Брат", "двоемыслие", "новояз") стали нарицательными и 
                используются для описания современных политических реалий.''',
                'price': Decimal('27.99'),
                'age_restriction': 16
            },
            {
                'title': 'Сто лет одиночества',
                'summary': '''Магический реализм в своем лучшем проявлении - роман колумбийского писателя 
                Габриэля Гарсиа Маркеса рассказывает историю семьи Буэндиа на протяжении семи поколений. 
                В затерянном городке Макондо разворачивается сага, где реальность переплетается с фантастикой, 
                а обыденное соседствует с чудесным. Автор создает уникальный мир, населенный яркими персонажами, 
                каждый из которых несет свое бремя одиночества. Роман исследует темы любви и войны, 
                прогресса и традиций, жизни и смерти. Это произведение о цикличности истории, о том, 
                как прошлое влияет на настоящее, и о неизбежности судьбы, от которой невозможно убежать.''',
                'price': Decimal('26.99'),
                'age_restriction': 16
            }
        ]

        for book_data in books_data:
            book = Book.objects.create(
                title=book_data['title'],
                summary=book_data['summary'],
                imprint='Эксмо',
                ISBN=f'978-3-16-{random.randint(100000, 999999)}-0',
                price=book_data['price'],
                age_restriction=book_data['age_restriction'],
                language=russian
            )
            book.author.set(random.sample(list(authors), random.randint(1, 2)))
            book.genre.set(random.sample(list(genres), random.randint(1, 3)))
            book.save()

        # Обновляем количество экземпляров для каждой книги
        for book in Book.objects.all():
            book.quantity = random.randint(5, 20)
            book.save()
            self.stdout.write(self.style.SUCCESS(f'Updated quantity for book: {book.title}'))

        # Создаем информацию о компании
        self.stdout.write('Creating company info...')
        CompanyInfo.objects.create(
            name='Книжный магазин',
            description='Лучший книжный магазин в городе',
            history='Основан в 2025 году. Мы стремимся предоставить нашим клиентам лучший выбор книг и высокий уровень сервиса.',
            requisites='ИНН: 1234567890'
        )

        # Создаем статьи
        self.stdout.write('Creating articles...')
        articles_data = [
            ('Новое поступление книг', 'Большое поступление новинок литературы', 'Рады сообщить о поступлении новых книг в наш магазин.'),
            ('Встреча с автором', 'Приглашаем на встречу с известным писателем', 'В нашем магазине состоится встреча с популярным автором.'),
            ('Скидки на классику', 'Весенние скидки на классическую литературу', 'Специальные цены на классические произведения.'),
            ('Детский праздник', 'Праздник для юных читателей', 'Приглашаем детей и родителей на праздник книги.'),
            ('Книжный клуб', 'Открытие книжного клуба', 'Начинает работу наш книжный клуб для любителей литературы.'),
            ('Конкурс рецензий', 'Объявляем конкурс книжных рецензий', 'Участвуйте в нашем конкурсе и выигрывайте призы.'),
            ('Новый раздел', 'Открытие раздела научной литературы', 'Теперь в нашем магазине представлен широкий выбор научной литературы.'),
            ('Подарочные карты', 'Подарочные карты к праздникам', 'Порадуйте близких подарочной картой нашего магазина.'),
            ('Доставка книг', 'Запуск службы доставки', 'Теперь доставляем книги по всему городу.'),
            ('Акция месяца', 'Специальные предложения июня 2025', 'Весь июнь действуют специальные цены на избранные книги.'),
        ]

        for title, short_desc, content in articles_data:
            Article.objects.create(
                title=title,
                short_description=short_desc,
                content=content,
                is_published=True
            )

        # Создаем термины
        self.stdout.write('Creating terms...')
        terms_data = [
            ('Что такое ISBN?', 'ISBN - это уникальный номер книжного издания.'),
            ('Что такое УДК?', 'УДК - универсальная десятичная классификация книг.'),
            ('Что такое ББК?', 'ББК - библиотечно-библиографическая классификация.'),
            ('Что такое авторский лист?', 'Единица измерения объема текста, равная 40000 печатных знаков.'),
            ('Что такое аннотация?', 'Краткое содержание книги.'),
            ('Что такое форзац?', 'Двойной лист бумаги, соединяющий книжный блок с переплетной крышкой.'),
            ('Что такое суперобложка?', 'Дополнительная обложка поверх переплета.'),
            ('Что такое экслибрис?', 'Книжный знак, указывающий на принадлежность книги определенному владельцу.'),
            ('Что такое фронтиспис?', 'Иллюстрация в начале книги.'),
            ('Что такое колофон?', 'Текст на последней странице книги с выходными данными издания.'),
        ]

        for question, answer in terms_data:
            Term.objects.create(question=question, answer=answer)

        # Создаем промокоды
        self.stdout.write('Creating promo codes...')
        promo_data = [
            ('WELCOME2025', 'Скидка для новых клиентов', 10),
            ('SPRING2025', 'Весенняя скидка', 15),
            ('SUMMER2025', 'Летняя скидка', 20),
            ('BIRTHDAY2025', 'Скидка в день рождения', 25),
            ('BOOKS2025', 'Скидка на все книги', 5),
        ]

        for code, desc, discount in promo_data:
            PromoCode.objects.create(
                code=code,
                description=desc,
                discount=discount,
                valid_from=timezone.now(),
                valid_to=timezone.now() + timedelta(days=90),
                is_active=True
            )

        # Создаем отзывы
        self.stdout.write('Creating reviews...')
        reviews_data = [
            (admin_user, 5, 'Отличный магазин! Большой выбор книг и отличное обслуживание.'),
            (test_user, 4, 'Хороший выбор книг, но хотелось бы больше новинок.'),
            (admin_user, 5, 'Очень доволен покупками. Всегда есть интересные акции.'),
            (test_user, 3, 'В целом неплохо, но есть над чем поработать.'),
            (admin_user, 4, 'Удобный сайт, быстрая доставка.'),
            (test_user, 5, 'Прекрасный ассортимент классической литературы!'),
            (admin_user, 4, 'Хорошие цены и частые скидки.'),
            (test_user, 5, 'Отзывчивый персонал, всегда помогут с выбором.'),
            (admin_user, 5, 'Регулярно заказываю здесь книги, всегда доволен.'),
            (test_user, 4, 'Хороший книжный магазин, рекомендую!'),
        ]

        for user, rating, text in reviews_data:
            Review.objects.create(
                user=user,
                rating=rating,
                text=text,
                is_published=True
            )

        # Создаем историю покупок
        users = User.objects.filter(is_staff=False)
        books = Book.objects.all()
        
        for _ in range(50):  # Создаем 50 случайных покупок
            user = random.choice(users)
            book = random.choice(books)
            quantity = random.randint(1, 3)
            days_ago = random.randint(1, 60)
            
            purchase_date = timezone.now() - timedelta(days=days_ago)
            
            PurchaseHistory.objects.create(
                user=user,
                book=book,
                quantity=quantity,
                purchase_date=purchase_date,
                total_price=book.price * quantity
            )
            
            self.stdout.write(self.style.SUCCESS(
                f'Created purchase history: {user.username} bought {quantity} copies of {book.title}'
            ))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database')) 