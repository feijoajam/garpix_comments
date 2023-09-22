from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


from app.settings import ACCEPTED_LIKE_MODELS

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='likes')
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content type'))
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def source(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def __str__(self):
        return "{}: {}".format(self.user, self.source)

    def save(self, *args, **kwargs):
        model_class = self.content_type.model_class()
        content_object = get_object_or_404(model_class, pk=self.object_id)
        if content_object._meta.model_name not in ACCEPTED_LIKE_MODELS:
            raise ValidationError(
                _('Model %s must be in ACCEPTED_LIKE_MODELS' % content_object._meta.model_name))
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (('user', 'content_type', 'object_id'),)
        verbose_name = _('Лайк')
        verbose_name_plural = _('Лайки')
