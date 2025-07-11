from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these fields in the list
    list_filter = ('author', 'publication_year')  # Add filters for easy browsing
    search_fields = ('title', 'author')  # Add search box for title and author
