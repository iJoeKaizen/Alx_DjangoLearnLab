from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture", "followers"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # ✅ ensures password is write-only

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # ✅ use create_user() so password is hashed
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        Token.objects.create(user=user)  # auto-generate token
        return user
