from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "target", "timestamp", "read"]

    def get_target(self, obj):
        if obj.target is None:
            return None
        # Provide simple representation
        ct = ContentType.objects.get_for_model(obj.target.__class__)
        return {
            "app_label": ct.app_label,
            "model": ct.model,
            "object_id": obj.target_object_id,
            "repr": str(obj.target)
        }
