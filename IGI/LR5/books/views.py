from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Book, Author, Genre, Language, BookInstance, Favorite, CartItem, PurchaseHistory
from .forms import BookForm, AuthorForm, GenreForm, LanguageForm, BookInstanceForm
from content.models import Article
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from django.db.models.functions import ExtractMonth
from statistics import mean, median, mode
from collections import Counter
from users.models import CustomUser
import json
import logging
from analytics.graph_utils import generate_pie_chart, generate_bar_chart
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

def staff_required(view_func):
    def check_staff(user):
        return user.is_authenticated and (user.is_staff or user.is_superuser)
    decorated_view = user_passes_test(check_staff, login_url='users:login')(view_func)
    return decorated_view

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    login_url = reverse_lazy('users:login')

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        book = self.get_object()

        instances = BookInstance.objects.filter(book=book)
        for instance in instances:
            instance.mark_as_viewed()

        return response

@staff_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Книга успешно создана.')
            return redirect('books:book-list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@staff_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Книга успешно обновлена.')
            return redirect('books:book-list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'book': book})

@staff_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга успешно удалена.')
        return redirect('books:book-list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# Author views
class AuthorListView(StaffRequiredMixin, ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(StaffRequiredMixin, DetailView):
    model = Author
    template_name = 'books/author_detail.html'

class AuthorCreateView(StaffRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'books/author_form.html'
    success_url = reverse_lazy('books:author-list')

class AuthorUpdateView(StaffRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'books/author_form.html'
    success_url = reverse_lazy('books:author-list')

class AuthorDeleteView(StaffRequiredMixin, DeleteView):
    model = Author
    template_name = 'books/author_confirm_delete.html'
    success_url = reverse_lazy('books:author-list')

# Genre views
class GenreListView(StaffRequiredMixin, ListView):
    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'

class GenreCreateView(StaffRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre-list')

class GenreUpdateView(StaffRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre-list')

class GenreDeleteView(StaffRequiredMixin, DeleteView):
    model = Genre
    template_name = 'books/genre_confirm_delete.html'
    success_url = reverse_lazy('books:genre-list')

# BookInstance views
class BookInstanceListView(StaffRequiredMixin, ListView):
    model = BookInstance
    template_name = 'books/bookinstance_list.html'
    context_object_name = 'bookinstances'

    def get_queryset(self):
        return BookInstance.objects.all().select_related('book')

class BookInstanceCreateView(StaffRequiredMixin, CreateView):
    model = BookInstance
    form_class = BookInstanceForm
    template_name = 'books/bookinstance_form.html'
    success_url = reverse_lazy('books:bookinstance-list')

class BookInstanceUpdateView(StaffRequiredMixin, UpdateView):
    model = BookInstance
    form_class = BookInstanceForm
    template_name = 'books/bookinstance_form.html'
    success_url = reverse_lazy('books:bookinstance-list')

class BookInstanceDeleteView(StaffRequiredMixin, DeleteView):
    model = BookInstance
    template_name = 'books/bookinstance_confirm_delete.html'
    success_url = reverse_lazy('books:bookinstance-list')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_calendar(self, year, month):
        months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]

        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        first_day = datetime(year, month, 1)

        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
            next_month = 1
            next_year = year + 1
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            next_month = month + 1
            next_year = year

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        num_days = last_day.day

        current_date = timezone.localtime().date()

        first_weekday = first_day.weekday()

        calendar_rows = []

        month_title = f"{months[month-1]} {year}"

        weekdays_row = weekdays

        current_day = 1
        current_row = ['  ' for _ in range(first_weekday)]

        while current_day <= num_days:
            while len(current_row) < 7 and current_day <= num_days:
                is_current = (current_day == current_date.day and
                            month == current_date.month and
                            year == current_date.year)

                day_str = f"{current_day:2d}"
                current_row.append({
                    'day': day_str,
                    'is_current': is_current
                })
                current_day += 1

            while len(current_row) < 7:
                current_row.append('  ')

            calendar_rows.append(current_row)
            current_row = []

        return {
            'title': month_title,
            'weekdays': weekdays_row,
            'rows': calendar_rows,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'current_month': month,
            'current_year': year
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_article'] = Article.objects.filter(is_published=True).order_by('-created_at').first()

        current_time = timezone.localtime()
        month = int(self.request.GET.get('month', current_time.month))
        year = int(self.request.GET.get('year', current_time.year))

        context['calendar'] = self.get_calendar(year, month)

        context['current_time'] = current_time
        context['timezone_name'] = current_time.tzinfo.key if hasattr(current_time.tzinfo, 'key') else str(current_time.tzinfo)

        return context

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'books/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

@login_required
def add_to_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added' if created else 'exists'})
    return redirect('books:book-detail', pk=pk)

@login_required
def remove_from_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    favorite.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    return redirect('books:favorites')

class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'books/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total = sum(item.total_price for item in cart_items)
        context['total'] = total
        return context

@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Check age restriction
    if request.user.date_of_birth:
        user_age = (timezone.now().date() - request.user.date_of_birth).days // 365
        if user_age < book.age_restriction:
            message = f'Извините, эта книга доступна только для пользователей старше {book.age_restriction} лет'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': message
                })
            messages.error(request, message)
            return redirect('books:book-detail', pk=pk)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    # Check available quantity
    available_quantity = book.get_available_quantity()
    current_cart_quantity = cart_item.quantity if not created else 0

    if current_cart_quantity < available_quantity:
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'added',
                'quantity': cart_item.quantity,
                'available_quantity': available_quantity
            })
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Недостаточно экземпляров в наличии',
                'available_quantity': available_quantity
            })

    return redirect('books:book-detail', pk=pk)

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    return redirect('books:cart')

@login_required
def update_cart_quantity(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Check available quantity
    available_quantity = cart_item.book.get_available_quantity()

    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({
            'status': 'removed',
            'message': 'Товар удален из корзины'
        })
    elif quantity > available_quantity:
        return JsonResponse({
            'status': 'error',
            'message': 'Недостаточно экземпляров в наличии',
            'available_quantity': available_quantity,
            'current_quantity': cart_item.quantity
        })
    else:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({
            'status': 'updated',
            'quantity': cart_item.quantity,
            'total': cart_item.total_price,
            'available_quantity': available_quantity
        })

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('books:cart')

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        if not delivery_method:
            messages.error(request, 'Выберите способ доставки')
            return redirect('books:cart')

        # Проверка возрастных ограничений
        for item in cart_items:
            if request.user.date_of_birth:
                user_age = (timezone.now().date() - request.user.date_of_birth).days // 365
                if user_age < item.book.age_restriction:
                    messages.error(
                        request,
                        f'Книга "{item.book.title}" доступна только для пользователей старше {item.book.age_restriction} лет'
                    )
                    return redirect('books:cart')

        # Проверка наличия
        for item in cart_items:
            if item.quantity > item.book.quantity:
                messages.error(
                    request,
                    f'Для книги "{item.book.title}" доступно только {item.book.quantity} экз.'
                )
                return redirect('books:cart')

        # Создание записей о покупках с учетом таймзоны
        current_time = timezone.now()
        for item in cart_items:
            PurchaseHistory.objects.create(
                user=request.user,
                book=item.book,
                quantity=item.quantity,
                total_price=item.total_price,
                delivery_method=delivery_method,
                created_at=current_time
            )
            item.book.quantity -= item.quantity
            item.book.save()

        # Очистка корзины
        cart_items.delete()

        messages.success(request, 'Заказ успешно оформлен!')
        return redirect('books:cart')

    return render(request, 'books/checkout.html', {
        'cart_items': cart_items,
        'total': sum(item.total_price for item in cart_items)
    })

class PurchaseHistoryView(StaffRequiredMixin, ListView):
    model = PurchaseHistory
    template_name = 'books/purchase_history.html'
    context_object_name = 'purchases'
    ordering = ['-created_at']

class StatisticsView(StaffRequiredMixin, TemplateView):
    template_name = 'books/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Список клиентов и их покупок
        customers = CustomUser.objects.filter(purchases__isnull=False).distinct().order_by('username')
        customer_stats = []
        for customer in customers:
            total_spent = customer.purchases.aggregate(total=Sum('total_price'))['total'] or 0
            customer_stats.append({
                'username': customer.username,
                'total_spent': total_spent,
                'purchase_count': customer.purchases.count()
            })

        # Список товаров и их продаж
        books = Book.objects.filter(purchases__isnull=False).distinct().order_by('title')
        book_stats = []
        for book in books:
            total_sales = book.purchases.aggregate(
                total=Sum('total_price'),
                quantity=Sum('quantity')
            )
            book_stats.append({
                'title': book.title,
                'total_sales': total_sales['total'] or 0,
                'quantity_sold': total_sales['quantity'] or 0
            })

        # Статистические показатели по продажам
        all_sales = [float(p.total_price) for p in PurchaseHistory.objects.all()]
        if all_sales:
            sales_stats = {
                'average': mean(all_sales),
                'median': median(all_sales),
                'mode': mode(all_sales) if len(all_sales) > 1 else all_sales[0]
            }
        else:
            sales_stats = {'average': 0, 'median': 0, 'mode': 0}

        # Статистика по возрасту клиентов
        customer_ages = []
        age_distribution = {}
        for customer in customers:
            if customer.date_of_birth:
                age = (timezone.now().date() - customer.date_of_birth).days // 365
                customer_ages.append(age)
                age_distribution[age] = age_distribution.get(age, 0) + 1

        age_stats = {
            'average': mean(customer_ages) if customer_ages else 0,
            'median': median(customer_ages) if customer_ages else 0
        }

        # Данные для графика возрастного распределения
        sorted_ages = sorted(age_distribution.items())
        age_labels = [str(age) for age, _ in sorted_ages]
        age_data = [count for _, count in sorted_ages]

        # Популярность и прибыльность жанров
        genre_popularity = {}
        genre_profit = {}
        for purchase in PurchaseHistory.objects.all():
            for genre in purchase.book.genre.all():
                if genre.name not in genre_popularity:
                    genre_popularity[genre.name] = 0
                    genre_profit[genre.name] = 0
                genre_popularity[genre.name] += purchase.quantity
                genre_profit[genre.name] += float(purchase.total_price)

        # Данные для графика распределения по жанрам
        genre_labels = list(genre_popularity.keys())
        genre_data = list(genre_popularity.values())

        most_popular_genre = max(genre_popularity.items(), key=lambda x: x[1]) if genre_popularity else ('Нет данных', 0)
        most_profitable_genre = max(genre_profit.items(), key=lambda x: x[1]) if genre_profit else ('Нет данных', 0)

        # Если нет данных, используем демо-данные
        if not genre_labels:
            genre_labels = ['Фантастика', 'Роман', 'Детектив', 'Научная литература', 'Поэзия']
            genre_data = [30, 25, 20, 15, 10]
            logger.info("Using demo data for genres")

        if not age_labels:
            age_labels = ['14-18', '19-25', '26-35', '36-45', '46+']
            age_data = [15, 30, 25, 20, 10]
            logger.info("Using demo data for ages")

        # Генерация графиков с помощью matplotlib
        genre_chart = generate_pie_chart(
            labels=genre_labels,
            data=genre_data,
            title='Распределение по жанрам'
        )

        age_chart = generate_bar_chart(
            labels=age_labels,
            data=age_data,
            title='Возрастное распределение покупателей',
            xlabel='Возраст',
            ylabel='Количество покупателей'
        )

        context.update({
            'customer_stats': customer_stats,
            'book_stats': book_stats,
            'sales_stats': sales_stats,
            'age_stats': age_stats,
            'most_popular_genre': most_popular_genre,
            'most_profitable_genre': most_profitable_genre,
            'genre_chart': genre_chart,
            'age_chart': age_chart
        })

        return context

@login_required
def get_updated_charts(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Получаем данные для графиков (копируем логику из StatisticsView)
    customers = CustomUser.objects.filter(purchases__isnull=False).distinct()

    # Статистика по возрасту клиентов
    age_distribution = {}
    for customer in customers:
        if customer.date_of_birth:
            age = (timezone.now().date() - customer.date_of_birth).days // 365
            age_distribution[age] = age_distribution.get(age, 0) + 1

    # Данные для графика возрастного распределения
    sorted_ages = sorted(age_distribution.items())
    age_labels = [str(age) for age, _ in sorted_ages]
    age_data = [count for _, count in sorted_ages]

    # Популярность жанров
    genre_popularity = {}
    for purchase in PurchaseHistory.objects.all():
        for genre in purchase.book.genre.all():
            if genre.name not in genre_popularity:
                genre_popularity[genre.name] = 0
            genre_popularity[genre.name] += purchase.quantity

    # Данные для графика распределения по жанрам
    genre_labels = list(genre_popularity.keys())
    genre_data = list(genre_popularity.values())

    # Если нет данных, используем демо-данные
    if not genre_labels:
        genre_labels = ['Фантастика', 'Роман', 'Детектив', 'Научная литература', 'Поэзия']
        genre_data = [30, 25, 20, 15, 10]

    if not age_labels:
        age_labels = ['14-18', '19-25', '26-35', '36-45', '46+']
        age_data = [15, 30, 25, 20, 10]

    # Генерация графиков
    genre_chart = generate_pie_chart(
        labels=genre_labels,
        data=genre_data,
        title='Распределение по жанрам'
    )

    age_chart = generate_bar_chart(
        labels=age_labels,
        data=age_data,
        title='Возрастное распределение покупателей',
        xlabel='Возраст',
        ylabel='Количество покупателей'
    )

    return JsonResponse({
        'genre_chart': genre_chart,
        'age_chart': age_chart
    })
