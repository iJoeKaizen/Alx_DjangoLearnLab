from .models import Notification
from django.contrib.contenttypes.models import ContentType

from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, NotificationMarkAllReadView


def create_notification(recipient, actor, verb, target=None):
    """
    Create a notification. `target` can be any model instance (Post, Comment, etc.).
    """
    nt_kwargs = {
        "recipient": recipient,
        "actor": actor,
        "verb": verb,
    }
    if target is not None:
        nt_kwargs["target_content_type"] = ContentType.objects.get_for_model(target.__class__)
        nt_kwargs["target_object_id"] = target.pk
    return Notification.objects.create(**nt_kwargs)


urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("<int:pk>/mark-read/", NotificationMarkReadView.as_view(), name="notification-mark-read"),
    path("mark-all-read/", NotificationMarkAllReadView.as_view(), name="notifications-mark-all-read"),
]
