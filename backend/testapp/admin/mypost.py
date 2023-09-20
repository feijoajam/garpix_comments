from django.contrib import admin

from testapp.models import MyPost


# from ..models import MyPost


@admin.register(MyPost)
class MyPostAdmin(admin.ModelAdmin):
    pass
