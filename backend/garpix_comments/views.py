from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from garpix_comments.models.comment import Comment, Like
from .serializers import CommentSerializer, CommentCreateSerializer, LikeSerializer


class CommentsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'likes':
            return LikeSerializer
        return CommentSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("content_type", int),
            OpenApiParameter("object_id", int),
        ]
    )
    def list(self, request, *args, **kwargs):
        object_id = self.request.GET.get('object_id', None)
        content_type = self.request.GET.get('content_type', None)
        if object_id and content_type:
            self.queryset = super().get_queryset().filter(object_id=object_id, content_type=content_type)
        return super().list(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        comment = self.get_object()
        user = self.request.user
        try:
            Like.objects.get(comment=comment, user=user).delete()
            return Response({'status': 'deleted'})
        except Like.DoesNotExist:
            Like.objects.create(comment=comment, user=user)
            return Response({'status': 'created'})

    @action(methods=['GET'], detail=True)
    def likes(self, request, pk, *args, **kwargs):
        queryset = Like.objects.filter(comment=self.get_object())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter("level", int),
        ]
    )
    @action(methods=['GET'], detail=True)
    def get_child_comments(self, request, pk, *args, **kwargs):
        node = self.get_object()
        level = self.request.GET.get('level', None)
        queryset = node.get_descendants().filter(level__lte=node.level + int(level))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
