from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Sum, F, Func
from django.db.models.functions import ExtractYear, TruncDate, ExtractHour
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from statistics import median, mode, mean
from collections import Counter
from users.models import CustomUser
from books.models import BookInstance, Book, PurchaseHistory
from .models import Sale
from .forms import AnalyticsFilterForm, DateRangeForm
import calendar
import json
import logging
import pytz
from datetime import timedelta

logger = logging.getLogger('analytics')

# Create your views here.

class MedianFunc(Func):
    function = 'PERCENTILE_CONT'
    template = '%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)'

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff_member or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        logger.info(f'Запрос статистики от пользователя {self.request.user.username}')
        
        # Инициализируем формы
        filter_form = AnalyticsFilterForm(self.request.GET)
        date_range_form = DateRangeForm(self.request.GET)
        
        context['filter_form'] = filter_form
        context['date_range_form'] = date_range_form
        
        if not filter_form.is_valid():
            logger.warning(f'Невалидная форма фильтров: {filter_form.errors}')
            return context
            
        if not date_range_form.is_valid():
            logger.warning(f'Невалидная форма дат: {date_range_form.errors}')
            return context
        
        # Получаем очищенные данные из формы
        cleaned_data = filter_form.cleaned_data
        search_query = cleaned_data.get('search', '')
        sort_by = cleaned_data.get('sort', '-created_at')
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        logger.debug(f'Параметры фильтрации: search={search_query}, sort={sort_by}, date_from={date_from}, date_to={date_to}')
        
        # Текущая дата и время в timezone пользователя
        try:
            user_timezone = self.request.user.timezone
            current_time = timezone.localtime(timezone.now(), pytz.timezone(user_timezone))
        except Exception as e:
            logger.error(f'Ошибка при работе с timezone: {str(e)}')
            current_time = timezone.now()
            user_timezone = 'UTC'
        
        # Форматирование даты
        context['current_date'] = current_time.strftime("%d/%m/%Y")
        context['current_time'] = current_time.strftime("%H:%M:%S")
        context['timezone'] = user_timezone
        
        # Календарь
        cal = calendar.TextCalendar()
        context['calendar'] = cal.formatmonth(current_time.year, current_time.month)

        try:
            # Базовый QuerySet для продаж
            sales = Sale.objects.all()

            # Применяем фильтры поиска
            if search_query:
                sales = sales.filter(
                    book__title__icontains=search_query
                ) | sales.filter(
                    customer__username__icontains=search_query
                ) | sales.filter(
                    book__genre__name__icontains=search_query
                )
                logger.info(f'Применен поисковый фильтр: {search_query}')

            # Фильтрация по датам
            if date_from:
                sales = sales.filter(created_at__gte=date_from)
                logger.info(f'Применен фильтр по начальной дате: {date_from}')
            if date_to:
                sales = sales.filter(created_at__lte=date_to)
                logger.info(f'Применен фильтр по конечной дате: {date_to}')

            # Сортировка
            sales = sales.order_by(sort_by)
            logger.debug(f'Применена сортировка: {sort_by}')
            
            # Список клиентов с суммой покупок
            customers = CustomUser.objects.filter(role='customer')
            if search_query:
                customers = customers.filter(
                    username__icontains=search_query
                ) | customers.filter(
                    phone__icontains=search_query
                )
            
            customers = customers.annotate(
                total_purchases=Sum('sale__total', default=0)
            ).order_by('username')
            
            context['customers'] = customers
            
            if sales.exists():
                # Общая статистика
                total_sales = sales.aggregate(
                    total_amount=Sum('total'),
                    avg_sale=Avg('total'),
                    total_books=Sum('quantity')
                )
                
                # Список всех сумм продаж для расчета медианы и моды
                all_sales = list(sales.values_list('total', flat=True))
                
                context['total_sales'] = total_sales
                context['median_sale'] = median(all_sales)
                context['mode_sale'] = mode(all_sales)
                
                logger.info(f'Рассчитана общая статистика: всего продаж={total_sales["total_amount"]}, '
                          f'среднее={total_sales["avg_sale"]}, всего книг={total_sales["total_books"]}')
                
                # Статистика по возрасту клиентов
                age_stats = CustomUser.objects.filter(role='customer').aggregate(
                    avg_age=Avg('age'),
                    total_customers=Count('id')
                )
                
                all_ages = list(CustomUser.objects.filter(role='customer').values_list('age', flat=True))
                
                context['age_stats'] = age_stats
                context['median_age'] = median(all_ages) if all_ages else 0
                
                logger.info(f'Рассчитана статистика по клиентам: средний возраст={age_stats["avg_age"]}, '
                          f'всего клиентов={age_stats["total_customers"]}')
                
                # Популярные жанры
                popular_genres = sales.values(
                    'book__genre__name'
                ).annotate(
                    total_sold=Sum('quantity'),
                    total_revenue=Sum('total')
                ).order_by('-total_sold')
                
                context['popular_genres'] = popular_genres

                # Данные для графиков
                # Продажи по дням
                sales_by_date = sales.annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    total_sales=Sum('total'),
                    books_sold=Sum('quantity')
                ).order_by('date')

                # Продажи по жанрам
                sales_by_genre = list(popular_genres.values('book__genre__name', 'total_sold', 'total_revenue'))
                
                # Возрастные группы
                age_groups = CustomUser.objects.filter(role='customer').values('age').annotate(
                    count=Count('id')
                ).order_by('age')

                # Преобразуем данные для графиков в JSON
                try:
                    context['sales_by_date_json'] = json.dumps([{
                        'date': item['date'].strftime('%d/%m/%Y'),
                        'total_sales': float(item['total_sales']),
                        'books_sold': item['books_sold']
                    } for item in sales_by_date])

                    context['sales_by_genre_json'] = json.dumps([{
                        'genre': item['book__genre__name'],
                        'total_sold': item['total_sold'],
                        'total_revenue': float(item['total_revenue'])
                    } for item in sales_by_genre])

                    context['age_groups_json'] = json.dumps([{
                        'age': item['age'],
                        'count': item['count']
                    } for item in age_groups])

                    logger.info('Данные для графиков успешно подготовлены')
                    
                except Exception as e:
                    logger.error(f'Ошибка при подготовке данных для графиков: {str(e)}')
                    return JsonResponse({'error': str(e)}, status=500)
                
            # Медианное время на сайте
            one_month_ago = timezone.now() - timedelta(days=30)
            user_sessions = CustomUser.objects.filter(
                last_login__gte=one_month_ago
            ).annotate(
                session_duration=F('last_logout') - F('last_login')
            ).exclude(session_duration__isnull=True)

            if user_sessions.exists():
                median_duration = user_sessions.aggregate(
                    median_duration=MedianFunc('session_duration')
                )['median_duration']
                context['median_session_duration'] = median_duration

            # Распределение посещений по часам
            visits_by_hour = CustomUser.objects.filter(
                last_login__gte=one_month_ago
            ).annotate(
                hour=ExtractHour('last_login')
            ).values('hour').annotate(
                count=Count('id')
            ).order_by('hour')
            
            context['visits_by_hour'] = list(visits_by_hour)
            
            # Конверсия (отношение покупок к просмотрам)
            total_views = BookInstance.objects.filter(
                viewed_at__gte=one_month_ago
            ).count()
            
            total_purchases = Sale.objects.filter(
                created_at__gte=one_month_ago
            ).count()
            
            if total_views > 0:
                context['conversion_rate'] = (total_purchases / total_views) * 100
                
        except Exception as e:
            logger.error(f'Ошибка при расчете статистики: {str(e)}')
            context['error'] = str(e)

        return context

class StatisticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/statistics.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all purchases
        purchases = PurchaseHistory.objects.all()
        
        # Customers and products in alphabetical order with total sales
        customers = CustomUser.objects.filter(purchases__isnull=False).distinct().order_by('username')
        customer_sales = {}
        for customer in customers:
            total_sales = PurchaseHistory.objects.filter(user=customer).aggregate(
                total=Sum('total_price')
            )['total'] or 0
            customer_sales[customer.username] = total_sales
            
        # Statistical indicators for sales
        all_sales = [float(sale) for sale in purchases.values_list('total_price', flat=True)]
        sales_stats = {
            'mean': mean(all_sales) if all_sales else 0,
            'median': median(all_sales) if all_sales else 0,
            'mode': mode(all_sales) if all_sales else 0
        }
        
        # Customer age statistics
        current_year = timezone.now().year
        customer_ages = []
        age_distribution = {}
        for user in customers:
            if user.date_of_birth:
                age = current_year - user.date_of_birth.year
                customer_ages.append(age)
                age_distribution[age] = age_distribution.get(age, 0) + 1
        
        # Genre popularity and revenue
        genre_popularity = {}
        genre_profit = {}
        for purchase in purchases:
            for genre in purchase.book.genre.all():
                if genre.name not in genre_popularity:
                    genre_popularity[genre.name] = 0
                    genre_profit[genre.name] = 0
                genre_popularity[genre.name] += purchase.quantity
                genre_profit[genre.name] += float(purchase.total_price)
        
        # If no data, use demo data
        if not genre_popularity:
            genre_popularity = {
                'Фантастика': 30,
                'Роман': 25,
                'Детектив': 20,
                'Научная литература': 15,
                'Поэзия': 10
            }
        
        if not age_distribution:
            age_distribution = {
                '18-24': 15,
                '25-34': 30,
                '35-44': 25,
                '45-54': 20,
                '55+': 10
            }
        
        # Prepare data for charts
        genre_labels = list(genre_popularity.keys())
        genre_data = list(genre_popularity.values())
        age_labels = list(age_distribution.keys())
        age_data = list(age_distribution.values())
        
        most_popular_genre = max(genre_popularity.items(), key=lambda x: x[1])[0]
        most_profitable_genre = max(genre_profit.items(), key=lambda x: x[1])[0]
        
        context.update({
            'customer_sales': customer_sales,
            'sales_stats': sales_stats,
            'most_popular_genre': most_popular_genre,
            'most_profitable_genre': most_profitable_genre,
            'genre_labels': json.dumps(genre_labels),
            'genre_data': json.dumps(genre_data),
            'age_labels': json.dumps(age_labels),
            'age_data': json.dumps(age_data),
            'timezone': timezone.get_current_timezone().zone
        })
        
        return context
