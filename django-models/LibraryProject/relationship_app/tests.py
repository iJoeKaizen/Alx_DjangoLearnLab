from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

class AdminViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test users with different roles
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.admin_user, 
            role='Admin'
        )
        
        self.librarian_user = User.objects.create_user(
            username='librarian', 
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.librarian_user, 
            role='Librarian'
        )
        
        self.member_user = User.objects.create_user(
            username='member', 
            password='testpass123'
        )
        UserProfile.objects.create(
            user=self.member_user, 
            role='Member'
        )
        
        self.unauthenticated_client = Client()
        
        # Authenticated clients
        self.admin_client = Client()
        self.admin_client.login(username='admin', password='testpass123')
        
        self.librarian_client = Client()
        self.librarian_client.login(username='librarian', password='testpass123')
        
        self.member_client = Client()
        self.member_client.login(username='member', password='testpass123')

    def test_admin_access_with_proper_role(self):
        """Admin user should be able to access admin view"""
        response = self.admin_client.get(reverse('admin-view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Admin!')

    def test_librarian_denied_access(self):
        """Librarian user should be denied access to admin view"""
        response = self.librarian_client.get(reverse('admin-view'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_member_denied_access(self):
        """Member user should be denied access to admin view"""
        response = self.member_client.get(reverse('admin-view'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_unauthenticated_user_redirected(self):
        """Unauthenticated users should be redirected to login"""
        response = self.unauthenticated_client.get(reverse('admin-view'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            f"{reverse('login')}?next={reverse('admin-view')}"
        )

    def test_admin_template_used(self):
        """Correct template should be used for admin view"""
        response = self.admin_client.get(reverse('admin-view'))
        self.assertTemplateUsed(response, 'admin_view.html')

    def test_admin_content_visibility(self):
        """Admin-specific content should be visible to admin users"""
        response = self.admin_client.get(reverse('admin-view'))
        self.assertContains(response, 'This page is accessible only to users with Admin role')
        self.assertNotContains(response, 'Librarian content')
        self.assertNotContains(response, 'Member content')

    def test_url_resolution(self):
        """URL should correctly resolve to admin view"""
        url = reverse('admin-view')
        self.assertEqual(url, '/admin/')