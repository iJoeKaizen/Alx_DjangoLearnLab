# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedListView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    LikePostView,
    UnlikePostView

)

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    # DRF viewsets
    path("", include(router.urls)),

    # Class-based views for specific endpoints
    path("posts/list-create/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/detail/", PostDetailView.as_view(), name="post-detail"),
    path("comments/list-create/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("posts/<int:pk>/like/", LikePostView.as_view(), name="post-like"),
    path("posts/<int:pk>/unlike/", UnlikePostView.as_view(), name="post-unlike"),

    # Feed endpoint
    path("feed/", FeedListView.as_view(), name="feed"),
]
