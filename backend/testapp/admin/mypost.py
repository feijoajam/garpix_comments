from django.contrib import admin
from ..models import MyPost


@admin.register(MyPost)
class MyPostAdmin(admin.ModelAdmin):
    pass



