from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from garpix_comments.models.comment import Comment
from garpix_comments.models.like import Like
from garpix_comments.serializers import CommentSerializer, CommentReplySerializer, LikeSerializer, \
    CommentCreateSerializer


class CommentsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'reply':
            return CommentReplySerializer
        if self.action == 'likes':
            return LikeSerializer
        if self.action == 'create':
            return CommentCreateSerializer
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
        ct = ContentType.objects.get_for_model(comment)
        try:
            Like.objects.get(object_id=comment.id, content_type=ct, user=user).delete()
            return Response({'status': 'deleted'})
        except Like.DoesNotExist:
            Like.objects.create(object_id=comment.id, content_type=ct, user=user)
            return Response({'status': 'created'})

    def perform_reply(self, serializer, comment):
        serializer.validated_data['author'] = self.request.user
        serializer.validated_data['object_id'] = comment.object_id
        serializer.validated_data['content_type'] = comment.content_type
        serializer.validated_data['parent'] = comment
        serializer.save()

    @action(methods=['POST'], detail=True)
    def reply(self, request, pk, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_reply(serializer, self.get_object())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

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
