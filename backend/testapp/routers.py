from rest_framework.routers import DefaultRouter

from .views import MyPostView

router = DefaultRouter()

router.register(r'posts', MyPostView, basename='mypost')
