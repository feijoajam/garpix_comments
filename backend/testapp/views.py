from rest_framework import viewsets

from garpix_comments.views.commentlike import CommentLikeMixin
from testapp.models import MyPost
from testapp.serializers import MyPostSerializer


class MyPostView(viewsets.ModelViewSet, CommentLikeMixin):
    queryset = MyPost.objects.all()

    def get_serializer_class(self):
        return MyPostSerializer
