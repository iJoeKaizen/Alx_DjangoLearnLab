# advanced-api-project/api/models.py
from django.db import models

class Author(models.Model):
    """
    Represents a book author.
    - name: the author's full name as a human-readable string.
    Authors can have many associated Book instances (one-to-many).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book.
    - title: the title of the book.
    - publication_year: integer year the book was published.
    - author: a ForeignKey to Author establishing a one-to-many relationship.
      Setting related_name='books' enables reverse access: some_author.books.all()
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
