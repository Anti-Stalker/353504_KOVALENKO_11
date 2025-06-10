from django.urls import path, re_path
from . import views

app_name = 'api'

urlpatterns = [
    # Поиск книг
    path('books/search/', views.BookSearchView.as_view(), name='book-search'),
    
    # Детали книги (используем регулярное выражение для ID книги)
    re_path(r'^books/(?P<book_id>[a-zA-Z0-9_-]+)/$', 
            views.BookDetailView.as_view(), 
            name='book-detail'),
    
    # Погода
    path('weather/', views.WeatherView.as_view(), name='weather'),

    path('sales/statistics/', views.sales_statistics, name='sales-statistics'),
    path('books/<int:book_id>/', views.book_details, name='book-details'),
    path('genres/statistics/', views.genre_statistics, name='genre-statistics'),
    path('genres/<int:genre_id>/statistics/', views.genre_statistics, name='genre-detail-statistics'),
] 