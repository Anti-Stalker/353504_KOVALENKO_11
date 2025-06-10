from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+79991234567'})
    )
    age = forms.IntegerField(
        required=True,
        min_value=14,
        max_value=120,
        widget=forms.NumberInput(attrs={'placeholder': '18'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'age', 'address')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone

class CustomUserChangeForm(UserChangeForm):
    phone = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+79991234567'})
    )
    age = forms.IntegerField(
        required=True,
        min_value=14,
        max_value=120,
        widget=forms.NumberInput(attrs={'placeholder': '18'})
    )
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'age', 'address')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone 