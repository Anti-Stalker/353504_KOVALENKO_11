from django.core.management.base import BaseCommand
from django.utils import timezone
from content.models import PromoCode
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creates 10 different promotional codes'

    def handle(self, *args, **options):
        # List of promotional codes to create
        promo_data = [
            {
                'code': 'WELCOME25',
                'description': 'Скидка 25% для новых клиентов',
                'discount': 25,
                'days_valid': 30
            },
            {
                'code': 'SUMMER2024',
                'description': 'Летняя скидка 20% на все книги',
                'discount': 20,
                'days_valid': 92
            },
            {
                'code': 'BOOKWORM15',
                'description': 'Скидка 15% для любителей чтения',
                'discount': 15,
                'days_valid': 60
            },
            {
                'code': 'STUDENT10',
                'description': 'Скидка 10% для студентов',
                'discount': 10,
                'days_valid': 180
            },
            {
                'code': 'WEEKEND30',
                'description': 'Скидка 30% на выходных',
                'discount': 30,
                'days_valid': 7
            },
            {
                'code': 'FICTION20',
                'description': 'Скидка 20% на художественную литературу',
                'discount': 20,
                'days_valid': 45
            },
            {
                'code': 'SPRING15',
                'description': 'Весенняя скидка 15%',
                'discount': 15,
                'days_valid': 90
            },
            {
                'code': 'BIRTHDAY50',
                'description': 'Праздничная скидка 50%',
                'discount': 50,
                'days_valid': 3
            },
            {
                'code': 'BOOKS2024',
                'description': 'Скидка 25% на все книги',
                'discount': 25,
                'days_valid': 120
            },
            {
                'code': 'SPECIAL40',
                'description': 'Специальная скидка 40%',
                'discount': 40,
                'days_valid': 14
            }
        ]

        now = timezone.now()

        # Delete existing promo codes
        PromoCode.objects.all().delete()

        # Create new promo codes
        for promo in promo_data:
            PromoCode.objects.create(
                code=promo['code'],
                description=promo['description'],
                discount=promo['discount'],
                valid_from=now,
                valid_to=now + timedelta(days=promo['days_valid']),
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created promo code: {promo["code"]}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created all promotional codes!')
        ) 