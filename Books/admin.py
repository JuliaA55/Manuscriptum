from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre')
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author')
    ordering = ('id',)
