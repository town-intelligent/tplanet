from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    uuid = models.CharField(max_length = 30)
    img = models.TextField(blank = True, null = True)
    name = models.CharField(max_length = 30, blank = True, null = True)
    business_philosophy = models.TextField(blank = True, null = True)
    period = models.CharField(max_length = 30, blank = True, null = True)
    budget = models.IntegerField(default = 0, blank = True, null = True)
    relate_people = models.IntegerField(default = 0, blank = True, null = True)
    project_type = models.TextField(blank = True, null = True)
    motivation = models.TextField(blank = True, null = True)
    motivation_img = models.TextField(blank = True, null = True)
    project_planning = models.TextField(blank = True, null = True)
    project_planning_img = models.TextField(blank = True, null = True)

    # TODO: Modulize wiight model
    weight = models.TextField(blank = True, null = True)
    weight_description = models.TextField(blank = True, null = True)

    sr = models.TextField(blank = True, null = True)
    hoster = models.CharField(max_length = 20, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    org = models.TextField(blank = True, null = True)
    tel = models.CharField(max_length = 20, blank = True, null = True)
    location = models.TextField(blank = True,  null = True)
    status = models.IntegerField(default = 0, blank = True, null = True)
    project_a = models.CharField(max_length = 20, blank = True, null = True)
    project_b = models.CharField(max_length = 20, blank = True, null = True)
    philosophy = models.TextField(blank = True, null = True)

class Task(models.Model):
    obj_project = models.ForeignKey(Project, on_delete = models.CASCADE)
    parent_task = models.ForeignKey("self", on_delete = models.CASCADE, null = True, blank = True)
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    uuid = models.CharField(max_length = 30)
    type_task = models.IntegerField() # Default: SDGS vote
    name = models.CharField(max_length = 30)
    overview = models.TextField(blank = True)
    thumbnail = models.TextField(blank = True)
    content = models.TextField(blank = True)
    weight = models.TextField(blank = True)
    token = models.IntegerField()
    period = models.CharField(max_length = 30, null = True)
    gps_flag = models.BooleanField(blank = True, null = True, default = False)

class GPS(models.Model):
    obj_project = models.ForeignKey(Project, on_delete = models.CASCADE, blank = True, null = True)
    obj_task = models.ForeignKey(Task, on_delete = models.CASCADE)
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    gps = models.TextField(blank = True, null = True)
    created_at = models.DateField(auto_now_add = True)

class SROI(models.Model):
    obj_project = models.ForeignKey(Project, on_delete = models.CASCADE)
    visible = models.BooleanField(blank = True, null = True, default = False)
    file_id = models.CharField(max_length = 120, null = True)
