from rest_framework import serializers
from .models import Comment, Like
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


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

    def validate(self, attrs):
        content_type = attrs['content_type']
        object_id = attrs['object_id']
        model_class = content_type.model_class()

        content_object = get_object_or_404(model_class, pk=object_id)

        if content_object._meta.model_name not in ACCEPTED_COMMENT_MODELS:
            raise ValidationError(
                _('Model %s must be in ACCEPTED_COMMENT_MODELS' %  content_object._meta.model_name))

        return attrs

    class Meta:
        model = Comment
        fields = ("object_id", "text", "content_type")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
