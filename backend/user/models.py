from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from garpix_notify.mixins import UserNotifyMixin
from garpix_user.models import GarpixUser


class User(GarpixUser):
    pass

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
