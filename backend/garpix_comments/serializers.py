from rest_framework import serializers
from garpix_comments.models.comment import Comment
from django.conf import settings

from garpix_comments.models.like import Like

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


class CommentReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("text",)


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("text", "object_id", "content_type", "parent")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
