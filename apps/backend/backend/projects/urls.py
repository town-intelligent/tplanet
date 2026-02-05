from django.urls import path
from . import views

urlpatterns = [
    path("new", views.new_tasks),
    path("submit", views.submit_tasks),
    path("upload", views.upload),
    path("comment", views.comment),
    path("weight", views.get_project_weight),
    path("projects", views.list_projects),
    # path("<str:uuid>", views.get_tasks), # Depredate
    path("get/<str:uuid>", views.get_tasks),
    path("info/<str:uuid>", views.get_project_info),
    path("tasks", views.list_tasks),
    path("push_project_cover", views.push_project_cover),
    path("push_task_cover", views.push_task_cover),
    path("get_child_tasks", views.get_child_tasks),
    path("get_parent_task", views.get_parent_task),
    path("send_project", views.send_project),
    path("del_project", views.del_project),
    path("get_task_comment", views.get_task_comment),
    path("del_task", views.del_task),
    path("verify_task", views.verify_task),
    path("task_progress", views.task_progress),
    path("task_weight", views.get_task_weight),
    path("gps_set", views.gps_set),
    path("gps_get", views.gps_get),
    path("get_sroi", views.get_sroi),
    path("get_sroi_meta", views.get_sroi_meta),
    path("set_sroi", views.set_sroi),
]
