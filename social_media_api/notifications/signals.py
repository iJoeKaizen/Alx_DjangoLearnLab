from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like, Comment
from notifications.utils import create_notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.user
        recipient = post.author
        if actor != recipient:
            create_notification(recipient=recipient, actor=actor, verb="liked your post", target=post)

@receiver(post_delete, sender=Like)
def delete_like_notification(sender, instance, **kwargs):
    # optional: remove like notifications if like undone
    # naive approach: remove notifications with same actor/verb/target
    from notifications.models import Notification
    post = instance.post
    Notification.objects.filter(
        recipient=post.author,
        actor=instance.user,
        verb="liked your post",
        target_object_id=post.pk
    ).delete()


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.author
        recipient = post.author
        if actor != recipient:
            create_notification(recipient=recipient, actor=actor, verb="commented on your post", target=post)
