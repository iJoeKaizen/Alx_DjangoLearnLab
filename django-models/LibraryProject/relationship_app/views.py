from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library, Book, UserProfile

# Role-check helper
def check_role(role):
    def inner(user):
        return hasattr(user, 'userprofile') and user.userprofile.role == role
    return inner

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('member_view')  # Redirect based on role later if needed
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Admin-only view
@user_passes_test(check_role('Admin'))
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian-only view
@user_passes_test(check_role('Librarian'))
@login_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member-only view
@user_passes_test(check_role('Member'))
@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Example book listing view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
