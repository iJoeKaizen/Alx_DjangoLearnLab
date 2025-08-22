from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture", "followers"]


class RegisterSerializer(serializers.ModelSerializer):
    # ✅ CharField for password (write_only so it never shows up in responses)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # ✅ ensures password gets hashed properly
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        Token.objects.create(user=user)  # auto-generate token on registration
        return user


class LoginSerializer(serializers.Serializer):
    # ✅ both are CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
