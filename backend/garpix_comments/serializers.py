from rest_framework import serializers
from .models import Comment, Like
from django.conf import settings


try:
    ACCEPTED_COMMENT_MODELS = settings.ACCEPTED_COMMENT_MODELS
except AttributeError:
    raise AttributeError(
        'ACCEPTED_COMMENT_MODELS not found in settings.'
    )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("object_id", "text", "content_type", "parent")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
