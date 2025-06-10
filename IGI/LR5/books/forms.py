from django import forms
from .models import Book, Author, Genre, Language, BookInstance

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'imprint', 'ISBN', 'genre', 'language', 'price', 'unit', 'age_restriction', 'quantity']
        labels = {
            'title': 'Название книги',
            'author': 'Авторы',
            'summary': 'Краткое содержание',
            'imprint': 'Издательство',
            'ISBN': 'ISBN',
            'genre': 'Жанры',
            'language': 'Язык',
            'price': 'Цена (BYN)',
            'unit': 'Единица измерения',
            'age_restriction': 'Возрастное ограничение',
            'quantity': 'Количество',
        }
        help_texts = {
            'age_restriction': 'Укажите возрастное ограничение (от 0 до 21)',
            'ISBN': 'Введите ISBN книги (13 символов)',
            'quantity': 'Укажите количество экземпляров книги',
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'date_of_death']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']

class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'uniqueId', 'status', 'due_back']
        widgets = {
            'due_back': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        } 