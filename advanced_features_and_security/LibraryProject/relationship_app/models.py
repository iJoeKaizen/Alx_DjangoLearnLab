from django.db import models
from django.conf import settings
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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='Member'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Automatically create or update UserProfile on User create/update
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)


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
        settings.AUTH_USER_MODEL,
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
