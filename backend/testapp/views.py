from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from rest_framework import viewsets, permissions


from backend.testapp.models import MyPost
from backend.testapp.serializers import MyPostSerializer


class MyPostView(viewsets.ModelViewSet):
    queryset = MyPost.objects.all()
    serializer_class = MyPostSerializer
