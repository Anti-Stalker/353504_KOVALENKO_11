from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from django.conf import settings

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя автора")
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Дата смерти", null=True, blank=True)
    str_repr = models.CharField(max_length=300, verbose_name="Строковое представление", blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название жанра")
    str_repr = models.CharField(max_length=300, verbose_name="Строковое представление", blank=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название языка")
    str_repr = models.CharField(max_length=300, verbose_name="Строковое представление", blank=True)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=50, verbose_name="Единица измерения")
    short_name = models.CharField(max_length=10, verbose_name="Сокращение")
    
    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ManyToManyField(Author, related_name='books', verbose_name="Авторы")
    summary = models.TextField(verbose_name="Краткое содержание")
    imprint = models.CharField(max_length=200, verbose_name="Издательство")
    ISBN = models.CharField(max_length=13, verbose_name="ISBN")
    genre = models.ManyToManyField(Genre, verbose_name="Жанры")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name="Язык")
    str_repr = models.CharField(max_length=300, verbose_name="Строковое представление", blank=True)
    age_restriction = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(21)],
        help_text='Возрастное ограничение (0-21)'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Цена (BYN)"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество экземпляров",
        validators=[MinValueValidator(0)]
    )
    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Единица измерения"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def get_available_quantity(self):
        """Возвращает количество доступных экземпляров"""
        return self.quantity

class BookInstance(models.Model):
    class LoanStatus(models.TextChoices):
        MAINTENANCE = 'm', 'На обслуживании'
        ON_LOAN = 'o', 'Выдана'
        AVAILABLE = 'a', 'Доступна'
        RESERVED = 'r', 'Зарезервирована'

    uniqueId = models.CharField(max_length=32, unique=True, verbose_name="Уникальный идентификатор")
    due_back = models.DateField(null=True, blank=True, verbose_name="Дата возврата")
    status = models.CharField(
        max_length=1,
        choices=LoanStatus.choices,
        blank=True,
        default=LoanStatus.MAINTENANCE,
        verbose_name="Статус"
    )
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, verbose_name="Книга")
    str_repr = models.CharField(max_length=300, verbose_name="Строковое представление", blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"
        ordering = ['due_back']

    def __str__(self):
        return f'{self.uniqueId} ({self.book.title})'

    def mark_as_viewed(self):
        self.viewed_at = timezone.now()
        self.save()

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.user.username} - {self.book.title} ({self.quantity})'

    @property
    def total_price(self):
        return self.book.price * self.quantity

class PurchaseHistory(models.Model):
    DELIVERY_CHOICES = (
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    )
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='purchases')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='pickup')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'История покупок'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title} ({self.quantity} шт.)'
