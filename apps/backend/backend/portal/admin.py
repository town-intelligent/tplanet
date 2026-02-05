from django.contrib import admin
from .models import Comment
from .models import News

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "obj_user")

admin.site.register(Comment, CommentAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ("uuid", "obj_user")

admin.site.register(News, NewsAdmin)
