from django.contrib import admin

from backend.testapp.models import MyPost


# from ..models import MyPost


@admin.register(MyPost)
class MyPostAdmin(admin.ModelAdmin):
    pass
