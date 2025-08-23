from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import RegisterSerializer, UserSerializer, UserMiniSerializer

User = get_user_model()

# Register new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Login existing user
class LoginView(generics.GenericAPIView):
    serializer_class = RegisterSerializer  # reuse username/password

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


# Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        target = get_object_or_404(User, id=user_id)

        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add to following set
        request.user.following.add(target)
        request.user.save()

        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        target = get_object_or_404(User, id=user_id)

        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        request.user.save()

        return Response({"detail": f"You unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns the list of users the current user follows.
        """
        following_qs = request.user.following.all()
        serializer = UserMiniSerializer(following_qs, many=True, context={"request": request})
        return Response(serializer.data)


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns the list of users that follow the current user.
        """
        followers_qs = request.user.followers.all()
        serializer = UserMiniSerializer(followers_qs, many=True, context={"request": request})
        return Response(serializer.data)