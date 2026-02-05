from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.sign_up),
    path("signin", views.sign_in),
    path("verify_jwt", views.verify_jwt),
    path("forgot_password", views.forgot_password),
    path("get_group", views.get_group),
    path("set_group", views.set_group),
    path("list_accounts", views.list_accounts),
    path("delete", views.delete),
    path("oauth/google", views.google_login),
]
