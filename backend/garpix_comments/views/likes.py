from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from garpix_comments.models.like import Like
from garpix_comments.serializers import LikeSerializer


class LikesViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def get_serializer_class(self):
        return LikeSerializer

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
        serializer.validated_data['user'] = self.request.user
        serializer.save()
