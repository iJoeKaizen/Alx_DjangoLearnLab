from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer


User = get_user_model()


class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)


def post(self, request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)


def get(self, request):
    return Response(UserSerializer(request.user).data)


def put(self, request):
    serializer = UserSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def patch(self, request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)