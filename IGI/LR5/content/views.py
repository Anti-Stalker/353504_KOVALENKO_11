from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import (
    CompanyInfo, Article, Term, Employee, 
    Vacancy, Review, PromoCode
)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'content/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.objects.first()
        return context

class NewsListView(ListView):
    model = Article
    template_name = 'content/news_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

class NewsDetailView(DetailView):
    model = Article
    template_name = 'content/news_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

class TermsListView(ListView):
    model = Term
    template_name = 'content/terms_list.html'
    context_object_name = 'terms'
    paginate_by = 20

class ContactsView(TemplateView):
    template_name = 'content/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()
        return context

class PrivacyView(TemplateView):
    template_name = 'content/privacy.html'

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'content/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(is_active=True)

class ReviewListView(ListView):
    model = Review
    template_name = 'content/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем статистику по рейтингам
        ratings_stats = {}
        total_reviews = Review.objects.filter(is_published=True).count()
        
        if total_reviews > 0:
            for rating in range(5, 0, -1):
                count = Review.objects.filter(is_published=True, rating=rating).count()
                percentage = (count / total_reviews) * 100
                ratings_stats[rating] = {
                    'count': count,
                    'percentage': percentage
                }
        
        context['ratings_stats'] = ratings_stats
        context['total_reviews'] = total_reviews
        
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'content/review_form.html'
    fields = ['rating', 'text']
    success_url = reverse_lazy('content:reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'content/promo_list.html'
    context_object_name = 'promocodes'

    def get_queryset(self):
        now = timezone.now()
        return PromoCode.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_to__gte=now
        )

class FAQView(TemplateView):
    template_name = 'content/faq.html'
