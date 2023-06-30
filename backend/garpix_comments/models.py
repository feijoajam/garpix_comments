from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(models.Model):
    """
        Комментарии к сущности. Есть возможность ответа на верхнеуровневый комментарий, но не глубже.
    """
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    text = models.TextField(verbose_name='Описание', blank=True, default='')
    author = models.ForeignKey('user.User', verbose_name=_('Автор'), on_delete=models.CASCADE,
                               related_name='author')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content type'))
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def source(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def __str__(self):
        return "{}: {}".format(self.author, self.text)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = (('user', 'comment'),)
        verbose_name = _('Лайк')
        verbose_name_plural = _('Лайки')
