from django.db import models
from django.conf import settings
from books.models import Book
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from users.models import CustomUser

class Sale(models.Model):
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        related_name='sales'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        verbose_name="Книга",
        related_name='sales'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Цена за единицу (BYN)"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Общая сумма (BYN)"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата продажи"
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата доставки"
    )
    
    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.price_per_unit:
            self.price_per_unit = self.book.price
        self.total = self.price_per_unit * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Продажа {self.book.title} для {self.customer.username}"

    def get_formatted_created_at(self):
        """Возвращает дату создания в формате DD/MM/YYYY"""
        return self.created_at.strftime("%d/%m/%Y")

    def get_formatted_updated_at(self):
        """Возвращает дату обновления в формате DD/MM/YYYY"""
        return self.updated_at.strftime("%d/%m/%Y")
