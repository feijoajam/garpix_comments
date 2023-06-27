from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet

router = DefaultRouter()

router.register(r'comments', CommentsViewSet, basename='comments')
