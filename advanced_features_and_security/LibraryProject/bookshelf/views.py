from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .models import Book
from .forms import BookForm, ExampleForm

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # handle form.cleaned_data here
            return render(request, 'bookshelf/success.html', {'name': form.cleaned_data['name']})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})
