from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    fields = ['name', 'date_of_birth', 'date_of_death']
    search_fields = ['name']

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'display_genre', 'language')
    list_filter = ('genre', 'language')
    search_fields = ['title', 'author__name', 'ISBN']
    inlines = [BookInstanceInline]

    def display_authors(self, obj):
        return ', '.join([author.name for author in obj.author.all()[:3]])
    display_authors.short_description = 'Авторы'

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])
    display_genre.short_description = 'Жанры'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'uniqueId')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'uniqueId')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back')
        }),
    )
    search_fields = ['uniqueId', 'book__title']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
