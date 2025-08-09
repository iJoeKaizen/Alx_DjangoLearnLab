from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ------------------------
# READ-ONLY views (no authentication required)
# ------------------------
class BookListView(generics.ListAPIView):
    """
    GET: Returns a list of all books.
    Public access (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Returns a single book by its ID.
    Public access (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# ------------------------
# WRITE views (restricted to authenticated users)
# ------------------------

class BookCreateView(generics.CreateAPIView):
    """
    POST: Creates a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Hook to modify the save behavior if needed.
        For example, we could log who created the book.
        """
        serializer.save()  # no custom save logic here yet


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Updates an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook to modify save behavior on update.
        Could log who updated the record.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Deletes an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

