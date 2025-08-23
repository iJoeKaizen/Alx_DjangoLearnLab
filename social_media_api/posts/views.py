from rest_framework import status, viewsets, generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification
from .models import Post, Comment, Like
from .serializers import (PostListSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer)
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "title"]
    filterset_fields = ["author__id", "author__username"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["created_at", "updated_at"]
    filterset_fields = ["post", "author__id", "author__username"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


# class LikePostView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, *args, **kwargs):
#         # 1️⃣ Get the post or 404
#         post = get_object_or_404(Post, pk=pk)
#         user = request.user

#         # 2️⃣ Create a like if not already liked
#         like, created = Like.objects.get_or_create(user=user, post=post)
#         if not created:
#             return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

#         # 3️⃣ Create a notification for the post author
#         if post.author != user:  # avoid notifying self
#             Notification.objects.create(
#                 recipient=post.author,
#                 actor=user,
#                 verb="liked your post",
#                 target=post
#             )

#         serializer = LikeSerializer(like, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class UnlikePostView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, pk=pk)
#         user = request.user
#         try:
#             like = Like.objects.get(user=user, post=post)
#             like.delete()

#             # Remove notification if exists
#             Notification.objects.filter(
#                 recipient=post.author,
#                 actor=user,
#                 verb="liked your post",
#                 target=post
#             ).delete()

#             return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)
#         except Like.DoesNotExist:
#             return Response({"detail": "Not liked yet."}, status=status.HTTP_400_BAD_REQUEST)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        # ✅ Get the post or return 404
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # ✅ Create like if it doesn't exist
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

        serializer = LikeSerializer(like, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        # ✅ Get the post or return 404
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "Not liked yet."}, status=status.HTTP_400_BAD_REQUEST)