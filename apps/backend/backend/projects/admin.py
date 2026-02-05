from django.contrib import admin
from .models import Project, Task, GPS, SROI

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "name", "obj_user")

admin.site.register(Project, ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "obj_project", "uuid", "name", "parent_task")

admin.site.register(Task, TaskAdmin)

class GPSAdmin(admin.ModelAdmin):
    list_display = ("id", "obj_project", "gps")

admin.site.register(GPS, GPSAdmin)

class SROIAdmin(admin.ModelAdmin):
    list_display = ("obj_project", "visible", "file_id")

admin.site.register(SROI, SROIAdmin)
