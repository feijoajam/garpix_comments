from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from garpix_comments.models.comment import Comment
from garpix_comments.models.like import Like
from garpix_comments.serializers import CommentSerializer, CommentReplySerializer, LikeSerializer
from django.contrib.contenttypes.models import ContentType


class CommentLikeMixin(GenericViewSet):

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        source = self.get_object()
        ct = ContentType.objects.get_for_model(source)
        user = self.request.user
        try:
            Like.objects.get(object_id=source.id, content_type=ct, user=user).delete()
            return Response({'status': 'deleted'})
        except Like.DoesNotExist:
            Like.objects.create(object_id=source.id, content_type=ct, user=user)
            return Response({'status': 'created'})

    @action(methods=['GET'], detail=True)
    def likes(self, request, pk, *args, **kwargs):
        source = self.get_object()
        ct = ContentType.objects.get_for_model(source).id
        queryset = Like.objects.filter(object_id=source.id, content_type=ct)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(methods=['POST'], detail=True)
    def comment(self, request, *args, **kwargs):
        source = self.get_object()
        ct = ContentType.objects.get_for_model(source)
        user = self.request.user

        self.serializer_class = CommentReplySerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = user
        serializer.validated_data['object_id'] = source.id
        serializer.validated_data['content_type'] = ct
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk, *args, **kwargs):
        source = self.get_object()
        ct = ContentType.objects.get_for_model(source)
        queryset = Comment.objects.filter(object_id=source.id, content_type=ct)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)
