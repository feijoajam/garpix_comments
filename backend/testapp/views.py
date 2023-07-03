from rest_framework import viewsets


from backend.testapp.models import MyPost
from backend.testapp.serializers import MyPostSerializer


class MyPostView(viewsets.ModelViewSet):
    queryset = MyPost.objects.all()
    serializer_class = MyPostSerializer
