from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    jwt_token = models.CharField(max_length = 400)

class SocialAccount(models.Model):
    provider = models.CharField(max_length=200, default='google')
    unique_id = models.CharField(max_length=200)
    obj_users = models.ForeignKey(
        User, related_name='social', on_delete = models.CASCADE)
