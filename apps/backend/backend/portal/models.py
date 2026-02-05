from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    uuid = models.CharField(max_length = 30, null = True, blank = True)
    name = models.CharField(max_length = 30, null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    org = models.CharField(max_length = 30, null = True, blank = True)
    website = models.CharField(max_length = 100, null = True, blank = True)
    tel = models.CharField(max_length = 30, null = True, blank = True)
    comment = models.TextField(null = True, blank = True)
    sdgs = models.TextField(null = True, blank = True)

class News(models.Model):
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    uuid = models.CharField(max_length = 30, null = True, blank = True)
    title = models.TextField(null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    static = models.TextField(null = True, blank = True)
    period = models.CharField(max_length = 30, blank = True, null = True)
