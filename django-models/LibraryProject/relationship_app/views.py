from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library, Librarian

# ✅ Function-based view to list all books using Book.objects.all() and the full template path
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view to display a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
