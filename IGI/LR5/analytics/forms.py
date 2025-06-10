from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AnalyticsFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск...',
            'pattern': '[A-Za-zА-Яа-я0-9\s]{0,50}',
            'title': 'Только буквы, цифры и пробелы, максимум 50 символов'
        })
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', 'Новые сначала'),
            ('created_at', 'Старые сначала'),
            ('-total', 'По сумме (убыв.)'),
            ('total', 'По сумме (возр.)')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                'Дата начала не может быть позже даты окончания'
            )
        
        return cleaned_data

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        })
    )
    
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date().isoformat()
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    'Дата начала не может быть позже даты окончания'
                )
            
            # Проверяем, что диапазон не превышает 1 год
            date_diff = end_date - start_date
            if date_diff.days > 365:
                raise forms.ValidationError(
                    'Диапазон дат не может превышать 1 год'
                )
        
        return cleaned_data 