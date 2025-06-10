from django.test import TestCase
import pytest
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from users.models import CustomUser
from books.models import Book, Genre, Author
from .models import Sale
from decimal import Decimal
import json

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpass123',
        'phone': '+375 (29) 123-45-67',
        'age': 25,
        'role': 'staff'
    }

@pytest.fixture
def user(user_data):
    return CustomUser.objects.create_user(**user_data)

@pytest.fixture
def customer_data():
    return {
        'username': 'customer',
        'password': 'customer123',
        'phone': '+375 (29) 765-43-21',
        'age': 30,
        'role': 'customer'
    }

@pytest.fixture
def customer(customer_data):
    return CustomUser.objects.create_user(**customer_data)

@pytest.fixture
def genre():
    return Genre.objects.create(name='Test Genre')

@pytest.fixture
def author():
    return Author.objects.create(name='Test Author')

@pytest.fixture
def book(genre, author):
    book = Book.objects.create(
        title='Test Book',
        str_repr='Test Book'
    )
    book.genre.add(genre)
    book.author.add(author)
    return book

@pytest.fixture
def sale(book, customer):
    return Sale.objects.create(
        book=book,
        customer=customer,
        quantity=2,
        price=Decimal('29.99'),
        total=Decimal('59.98')
    )

@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_access_denied_for_anonymous(self, client):
        url = reverse('analytics:dashboard')
        response = client.get(url)
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

    def test_dashboard_access_denied_for_customer(self, client, customer):
        client.force_login(customer)
        url = reverse('analytics:dashboard')
        response = client.get(url)
        assert response.status_code == 403

    def test_dashboard_access_allowed_for_staff(self, client, user):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.parametrize('search_query', [
        'Test Book',
        'customer',
        'Test Genre'
    ])
    def test_dashboard_search(self, client, user, sale, search_query):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        response = client.get(url, {'search': search_query})
        assert response.status_code == 200
        content = response.content.decode()
        assert search_query in content

    @pytest.mark.parametrize('sort_by', [
        '-created_at',
        'created_at',
        '-total',
        'total'
    ])
    def test_dashboard_sorting(self, client, user, sale, sort_by):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        response = client.get(url, {'sort': sort_by})
        assert response.status_code == 200

    def test_dashboard_date_filtering(self, client, user, sale):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        today = timezone.now().date()
        response = client.get(url, {
            'date_from': today,
            'date_to': today
        })
        assert response.status_code == 200

    def test_dashboard_statistics_calculation(self, client, user, sale):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        response = client.get(url)
        assert response.status_code == 200
        
        # Проверяем наличие всех необходимых данных в контексте
        assert 'total_sales' in response.context
        assert 'median_sale' in response.context
        assert 'mode_sale' in response.context
        assert 'age_stats' in response.context
        assert 'popular_genres' in response.context
        
        # Проверяем корректность расчетов
        total_sales = response.context['total_sales']
        assert total_sales['total_amount'] == sale.total
        assert total_sales['total_books'] == sale.quantity

    def test_dashboard_charts_data(self, client, user, sale):
        client.force_login(user)
        url = reverse('analytics:dashboard')
        response = client.get(url)
        assert response.status_code == 200
        
        # Проверяем наличие данных для графиков
        assert 'sales_by_date_json' in response.context
        assert 'sales_by_genre_json' in response.context
        assert 'age_groups_json' in response.context
        
        # Проверяем, что данные можно распарсить как JSON
        sales_by_date = json.loads(response.context['sales_by_date_json'])
        sales_by_genre = json.loads(response.context['sales_by_genre_json'])
        age_groups = json.loads(response.context['age_groups_json'])
        
        assert len(sales_by_date) > 0
        assert len(sales_by_genre) > 0
        assert len(age_groups) > 0

@pytest.mark.django_db
class TestSaleModel:
    def test_sale_creation(self, book, customer):
        sale = Sale.objects.create(
            book=book,
            customer=customer,
            quantity=1,
            price=Decimal('29.99'),
            total=Decimal('29.99')
        )
        assert sale.pk is not None
        assert sale.total == sale.price * sale.quantity

    def test_sale_str_representation(self, sale):
        expected = f"Продажа {sale.book.title} для {sale.customer.username}"
        assert str(sale) == expected

    def test_sale_date_formatting(self, sale):
        created_at = sale.get_formatted_created_at()
        updated_at = sale.get_formatted_updated_at()
        
        assert isinstance(created_at, str)
        assert isinstance(updated_at, str)
        assert len(created_at) == 10  # DD/MM/YYYY
        assert len(updated_at) == 10  # DD/MM/YYYY
