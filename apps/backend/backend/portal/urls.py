from django.urls import path
from . import views

urlpatterns = [
    path("comment", views.submit_comment),
    path("comment_list", views.list_comment),
    path("comment_delete", views.delete_comment),
    path("comment_get", views.get_comment),
    path("new", views.mockup_new),
    path("get", views.mockup_get),
    path("news_create", views.news_create),
    path("news_list", views.news_list),
    path("news_get", views.news_get),
    path("news_delete", views.news_delete),
    path("upload_img", views.upload_img),
]
