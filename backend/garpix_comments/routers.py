from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, LikesViewSet

router = DefaultRouter()

router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'likes', LikesViewSet, basename='likes')
