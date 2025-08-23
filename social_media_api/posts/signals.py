# posts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        print(f"New post created: {instance.title}")
