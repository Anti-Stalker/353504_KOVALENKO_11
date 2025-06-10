from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone as django_timezone
from datetime import date

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Покупатель'),
        ('staff', 'Работник'),
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name="Роль")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name="Телефон",
        unique=True,
        error_messages={
            'unique': "Пользователь с таким номером телефона уже существует."
        }
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(120)],
        verbose_name="Возраст",
        help_text="Возраст должен быть от 18 до 120 лет",
        default=18
    )
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    timezone = models.CharField(max_length=50, default='Europe/Minsk', verbose_name="Часовой пояс")
    created_at = models.DateTimeField(default=django_timezone.now, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    api_key = models.CharField(max_length=100, blank=True)
    api_requests_count = models.PositiveIntegerField(default=0)
    last_logout = models.DateTimeField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_staff_member(self):
        return self.role == 'staff'

    def clean(self):
        super().clean()
        if not self.phone:
            raise ValidationError({'phone': 'Номер телефона обязателен.'})
        if not self.age:
            raise ValidationError({'age': 'Возраст обязателен.'})
        if self.age < 18:
            raise ValidationError({'age': 'Возраст должен быть не менее 18 лет.'})

    def get_age(self):
        if self.date_of_birth:
            today = django_timezone.now().date()
            return (today - self.date_of_birth).days // 365
        return None

    @property
    def role_display(self):
        if self.is_superuser:
            return 'Суперпользователь'
        elif self.is_staff_member:
            return 'Работник'
        elif self.is_authenticated:
            return 'Покупатель'
        return 'Гость'
