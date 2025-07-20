from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # CRUD book views with permission checks
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

    # Role-based views
    path('admin/', views.admin_view, name='admin-view'),
    path('librarian/', views.librarian_view, name='librarian-view'),
    path('member/', views.member_view, name='member-view'),
    
    # Authentication views
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='relationship_app/logout.html',
        next_page='login'
    ), name='logout'),
    path('register/', views.register, name='register'),
    
    # Book and library views
    path('books/', views.list_books, name='list-books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
