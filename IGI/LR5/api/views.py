from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import GoogleBooksAPI, WeatherAPI
from books.models import Book
import re
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from .decorators import api_auth_required
from books.models import Genre
from analytics.models import Sale
import logging

logger = logging.getLogger('api')

# Create your views here.

class BookSearchView(ListView):
    template_name = 'api/book_search.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            results = GoogleBooksAPI.search_books(query)
            if results and 'items' in results:
                return results['items']
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class BookDetailView(TemplateView):
    template_name = 'api/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = kwargs.get('book_id')
        context['book'] = GoogleBooksAPI.get_book_details(book_id)
        return context

class WeatherView(LoginRequiredMixin, TemplateView):
    template_name = 'api/weather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.address:
            # Извлекаем город из адреса с помощью регулярного выражения
            city_match = re.search(r'г\.\s*([^,]+)', user.address)
            if city_match:
                city = city_match.group(1)
                context['weather'] = WeatherAPI.get_weather(city)
                context['city'] = city
        return context

@api_auth_required
@require_http_methods(["GET"])
def sales_statistics(request):
    """
    API endpoint для получения статистики продаж
    """
    try:
        # Получаем параметры запроса
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Базовый QuerySet
        sales = Sale.objects.all()
        
        # Применяем фильтры по датам
        if start_date:
            sales = sales.filter(created_at__gte=start_date)
        if end_date:
            sales = sales.filter(created_at__lte=end_date)
            
        # Рассчитываем статистику
        stats = sales.aggregate(
            total_sales=Sum('total'),
            avg_sale=Avg('total'),
            total_books=Sum('quantity'),
            total_orders=Count('id')
        )
        
        # Статистика по жанрам
        genre_stats = sales.values(
            'book__genre__name'
        ).annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('total')
        ).order_by('-total_sold')
        
        response_data = {
            'status': 'success',
            'data': {
                'general_stats': stats,
                'genre_stats': list(genre_stats)
            }
        }
        
        logger.info(f'Успешный запрос статистики продаж: {request.user.username}')
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f'Ошибка при получении статистики продаж: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_auth_required
@require_http_methods(["GET"])
def book_details(request, book_id):
    """
    API endpoint для получения детальной информации о книге
    """
    try:
        book = Book.objects.get(id=book_id)
        
        # Статистика продаж книги
        sales_stats = Sale.objects.filter(book=book).aggregate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('total'),
            avg_price=Avg('price')
        )
        
        response_data = {
            'status': 'success',
            'data': {
                'id': book.id,
                'title': book.title,
                'authors': [author.name for author in book.author.all()],
                'genres': [genre.name for genre in book.genre.all()],
                'sales_stats': sales_stats
            }
        }
        
        logger.info(f'Успешный запрос информации о книге {book_id}: {request.user.username}')
        return JsonResponse(response_data)
        
    except Book.DoesNotExist:
        logger.warning(f'Попытка получить несуществующую книгу {book_id}: {request.user.username}')
        return JsonResponse({
            'status': 'error',
            'message': 'Книга не найдена'
        }, status=404)
        
    except Exception as e:
        logger.error(f'Ошибка при получении информации о книге {book_id}: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_auth_required
@require_http_methods(["GET"])
def genre_statistics(request, genre_id=None):
    """
    API endpoint для получения статистики по жанрам
    """
    try:
        if genre_id:
            # Статистика конкретного жанра
            genre = Genre.objects.get(id=genre_id)
            sales = Sale.objects.filter(book__genre=genre)
            
            stats = sales.aggregate(
                total_sold=Sum('quantity'),
                total_revenue=Sum('total'),
                avg_price=Avg('price'),
                total_books=Count('book', distinct=True)
            )
            
            response_data = {
                'status': 'success',
                'data': {
                    'genre': genre.name,
                    'stats': stats
                }
            }
            
        else:
            # Статистика по всем жанрам
            genres = Genre.objects.all()
            genre_stats = []
            
            for genre in genres:
                sales = Sale.objects.filter(book__genre=genre)
                stats = sales.aggregate(
                    total_sold=Sum('quantity'),
                    total_revenue=Sum('total'),
                    avg_price=Avg('price'),
                    total_books=Count('book', distinct=True)
                )
                
                genre_stats.append({
                    'genre': genre.name,
                    'stats': stats
                })
            
            response_data = {
                'status': 'success',
                'data': genre_stats
            }
        
        logger.info(f'Успешный запрос статистики по жанрам: {request.user.username}')
        return JsonResponse(response_data)
        
    except Genre.DoesNotExist:
        logger.warning(f'Попытка получить несуществующий жанр {genre_id}: {request.user.username}')
        return JsonResponse({
            'status': 'error',
            'message': 'Жанр не найден'
        }, status=404)
        
    except Exception as e:
        logger.error(f'Ошибка при получении статистики по жанрам: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
