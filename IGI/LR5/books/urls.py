from django.urls import path
from .views import (
    BookListView, BookDetailView,
    AuthorListView, AuthorDetailView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView,
    GenreListView, GenreCreateView, GenreUpdateView, GenreDeleteView,
    BookInstanceListView, BookInstanceCreateView, BookInstanceUpdateView, BookInstanceDeleteView,
    HomeView, FavoriteListView, CartView, PurchaseHistoryView, StatisticsView
)
from . import views

app_name = 'books'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.create_book, name='book-create'),
    path('books/<int:pk>/update/', views.edit_book, name='book-update'),
    path('books/<int:pk>/delete/', views.delete_book, name='book-delete'),
    
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/create/', GenreCreateView.as_view(), name='genre-create'),
    path('genres/<int:pk>/update/', GenreUpdateView.as_view(), name='genre-update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre-delete'),
    
    path('bookinstances/', BookInstanceListView.as_view(), name='bookinstance-list'),
    path('bookinstances/create/', BookInstanceCreateView.as_view(), name='bookinstance-create'),
    path('bookinstances/<int:pk>/update/', BookInstanceUpdateView.as_view(), name='bookinstance-update'),
    path('bookinstances/<int:pk>/delete/', BookInstanceDeleteView.as_view(), name='bookinstance-delete'),
    
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('favorites/add/<int:pk>/', views.add_to_favorite, name='add-to-favorite'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorite, name='remove-from-favorite'),
    
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:pk>/', views.update_cart_quantity, name='update-cart-quantity'),
    path('cart/checkout/', views.checkout, name='checkout'),
    
    path('purchase-history/', PurchaseHistoryView.as_view(), name='purchase-history'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('statistics/charts/', views.get_updated_charts, name='get_updated_charts'),
] 