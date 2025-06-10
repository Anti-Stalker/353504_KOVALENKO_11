from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('terms/', views.TermsListView.as_view(), name='terms'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/add/', views.ReviewCreateView.as_view(), name='review-add'),
    path('promo/', views.PromoCodeListView.as_view(), name='promo'),
] 