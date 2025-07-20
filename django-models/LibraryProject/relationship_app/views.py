from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
    permission_required, 
    login_required, 
    user_passes_test
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import DetailView
from .models import Book, Library, Author
from .forms import BookForm



# --- 🔒 Role Helper Decorator ---
def check_role(required_role):
    def decorator(user):
        return (
            user.is_authenticated and
            hasattr(user, 'userprofile') and 
            user.userprofile.role == required_role
        )
    return decorator


# --- 📚 Book CRUD Views ---
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form, 'action': 'Add'})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'action': 'Edit'})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list-books')
    return render(request, 'book_confirm_delete.html', {'book': book})


# --- 📄 Book List ---
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})


# --- 🧑‍💼 Role-Based Views ---
@login_required
@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'admin_view.html')


@login_required
@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'librarian_view.html')


@login_required
@user_passes_test(check_role('Member'))
def member_view(request):
    return render(request, 'member_view.html')


# --- 🏛️ Library Detail View ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# --- 📝 Registration View ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect based on role
            role = getattr(user.userprofile, 'role', 'Member')
            if role == 'Admin':
                return redirect('admin-view')
            elif role == 'Librarian':
                return redirect('librarian-view')
            else:
                return redirect('member-view')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
