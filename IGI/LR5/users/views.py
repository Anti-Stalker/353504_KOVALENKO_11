from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.contrib import messages

# Create your views here.

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('books:book-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

@require_POST
def set_timezone(request):
    try:
        data = json.loads(request.body)
        timezone = data.get('timezone')
        if request.user.is_authenticated:
            request.user.timezone = timezone
            request.user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = '/'  # Redirect to home page after logout
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('users:login')
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Отправляем письмо для сброса пароля
        response = super().form_valid(form)
        # Добавляем сообщение об успешной отправке
        messages.success(
            self.request,
            'Инструкции по сбросу пароля отправлены на указанный email. '
            'Проверьте свою почту и следуйте инструкциям в письме.'
        )
        return redirect('users:login')