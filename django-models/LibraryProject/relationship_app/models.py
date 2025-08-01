from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# UserProfile with Role-based Access
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='userprofile'  # Easy access via user.userprofile
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='Member'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Automatically create or update UserProfile when a User is created or updated
@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
        else:
            UserProfile.objects.create(user=instance)


# Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        return self.title


# Library Model
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book, 
        related_name='libraries',
        blank=True
    )
    
    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name


# Librarian Model
class Librarian(models.Model):
    user = models.OneToOneField(
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
