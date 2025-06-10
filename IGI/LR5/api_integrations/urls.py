from django.urls import path
from . import views

app_name = 'api_integrations'

urlpatterns = [
    path('', views.api_page, name='api_page'),
    path('cat-fact/', views.get_new_cat_fact, name='get_cat_fact'),
    path('predict-nationality/', views.predict_nationality, name='predict_nationality'),
] 