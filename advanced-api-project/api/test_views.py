from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Create some sample books
        self.book1 = Book.objects.create(
            title="Book One", author="Author A", published_date="2020-01-01"
        )
        self.book2 = Book.objects.create(
            title="Book Two", author="Author B", published_date="2021-01-01"
        )

        # URLs
        self.list_url = reverse("book-list")  # from DRF router
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])
        self.create_url = reverse("book-list")
        self.update_url = lambda pk: reverse("book-detail", args=[pk])
        self.delete_url = lambda pk: reverse("book-detail", args=[pk])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "Author C",
            "published_date": "2022-01-01"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    def test_update_book(self):
        data = {
            "title": "Updated Title",
            "author": "Author A",
            "published_date": "2020-01-01"
        }
        response = self.client.put(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filter_books(self):
        response = self.client.get(f"{self.list_url}?author=Author A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author A")

    def test_search_books(self):
        response = self.client.get(f"{self.list_url}?search=Book Two")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book Two")

    def test_order_books(self):
        response = self.client.get(f"{self.list_url}?ordering=-published_date")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Book Two")

    def test_permission_required_for_create(self):
        self.client.logout()
        data = {
            "title": "Unauthorized Book",
            "author": "Author X",
            "published_date": "2023-01-01"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
