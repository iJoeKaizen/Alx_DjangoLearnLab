from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='userprofile'  # Add related_name for easier access
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='Member'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates UserProfile on User save
    More efficient single signal handler
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Safely update existing profile if it exists
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
        else:
            # Create profile if missing (shouldn't happen but safe)
            UserProfile.objects.create(user=instance)

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']  # Default ordering

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    class Meta:
        ordering = ['title']  # Default ordering
        indexes = [
            models.Index(fields=['title']),  # Add index for performance
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book, 
        related_name='libraries',
        blank=True  # Allow empty libraries
    )
    
    class Meta:
        verbose_name_plural = "Libraries"  # Proper plural name

    def __str__(self):
        return self.name

class Librarian(models.Model):
    user = models.OneToOneField(  # Link to User model instead of name
        User,
        on_delete=models.CASCADE,
        related_name='librarian_profile',
        null=True,
        blank=True
    )
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        related_name='librarian'
    )
    
    def __str__(self):
        return self.user.username if self.user else "Unassigned Librarian"