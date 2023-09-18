from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Comment


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass

@admin.register(Comment)
class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
