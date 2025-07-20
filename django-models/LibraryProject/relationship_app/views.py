from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library, Book, UserProfile


# def check_role_admin(user):
#     return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def check_role(role_name):
    def decorator(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role_name
    return decorator

def check_role_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def check_role_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


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

# Example book listing view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
