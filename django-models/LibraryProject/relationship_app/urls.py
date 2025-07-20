from django.urls import path
from . import views
from .views import list_books, add_book, edit_book, delete_book
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Role-based views - standardized naming convention
    path('admin/', views.admin_view, name='admin-view'),
    path('librarian/', views.librarian_view, name='librarian-view'),
    path('member/', views.member_view, name='member-view'),

       # Book CRUD URLs
     # Book CRUD URLs
    path('books/add/', views.add_book, name='add-book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit-book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete-book'),
    path('books/', views.list_books, name='list-books'),
    
    # Authentication views
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='relationship_app/logout.html',
        next_page='login'  # Redirect to login after logout
    ), name='logout'),
    path('register/', views.register, name='register'),
    
    # Book and library views
    path('books/', list_books, name='list-books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]