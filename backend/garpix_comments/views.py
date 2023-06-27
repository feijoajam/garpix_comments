from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
import requests
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import get_object_or_404

from .models import Comment, Like
from .serializers import CommentSerializer, CommentCreateSerializer, LikeSerializer


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='object_id', type=int, required=False),
#         OpenApiParameter(name='source_type', type=int, required=False)
#     ]
# )


# class CommentsViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
class CommentsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'likes':
            return LikeSerializer
        return CommentSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("source_type", int),
            OpenApiParameter("object_id", int),
        ]
    )
    def get_queryset(self, *args, **kwargs):
        object_id = self.request.GET.get('object_id', None)
        source_type = self.request.GET.get('source_type', None)
        if object_id and source_type:
            return Comment.objects.filter(object_id=object_id, source_type=source_type)
        return Comment.objects.all()

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
