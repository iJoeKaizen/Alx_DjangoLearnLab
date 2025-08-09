from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Serializes all fields of Book.
    Includes validation to prevent a publication_year in the future.
    """
    class Meta:
        model = Book
        fields = ('id', 'title', 'publication_year', 'author')

    def validate_publication_year(self, value):
        """
        Ensure publication_year is not in the future.
        Raises a ValidationError if the provided year > current year.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    - name: direct field from Author.
    - books: nested list that serializes all related Book instances.
      We set read_only=True here to return nested Book data without allowing nested
      creation through this serializer by default. If you want create/update nested
      behavior, we can implement custom create/update methods.
    Relationship handling:
    The Book model's ForeignKey uses related_name='books', so this serializer
    uses that reverse relation to fetch the books.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'books')
