import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from .manager import TaskManager, ProjectManager
from .SROI.sroi import SROIManager
from .gmail import send_gmail as send_gmail

@csrf_exempt
def new_tasks(request):
    # Get request
    req = request.POST.dict()

    # Get Task content
    obj_task_manager = TaskManager()
    result, content = obj_task_manager.create_task(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write(content)

        return response

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "task":content}))

    return response

@csrf_exempt
def get_tasks(request, uuid):
    # Get Task content
    obj_task_manager = TaskManager()
    result, task_content = obj_task_manager.get(uuid)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Task not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(task_content)

    return response

@csrf_exempt
def submit_tasks(request):
    # Get request
    req = request.POST.dict()

    # Get Task content
    obj_task_manager = TaskManager()
    result, content = obj_task_manager.submit(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Task not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def get_project_weight(request):
    # Get request
    req = request.POST.dict()

    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.weight(req["uuid"])

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def comment(request):
    # Get request
    req = request.POST.dict()

    # Get Task content
    obj_task_manager = TaskManager()
    result, content = obj_task_manager.comment(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Task comment fail")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def get_project_weight(request):
    # Get request
    req = request.POST.dict()

    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.weight(req["uuid"])

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def upload(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.upload(req)

    if result == False:
       response = HttpResponseBadRequest()
       response["Access-Control-Allow-Origin"] = "*"
       response.write("Invalid Field")

       return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def get_project_info(request, uuid):
    # Get Project content
    obj_project_manager = ProjectManager()
    result, project_content = obj_project_manager.get(uuid)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Project not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(project_content)

    return response

@csrf_exempt
def list_tasks(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_project_manager = ProjectManager()
    result, project_content = obj_project_manager.list_tasks(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Project not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(project_content)

    return response

@csrf_exempt
def list_projects(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_project_manager = ProjectManager()
    result, project_content = obj_project_manager.list_projects(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Account not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(project_content)

    return response

@csrf_exempt
def push_project_cover(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_project_manager = ProjectManager()
    result, project_content = obj_project_manager.push_project_cover(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Account not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(project_content)

    return response

@csrf_exempt
def push_task_cover(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_task_manager = TaskManager()
    result, task_content = obj_task_manager.push_task_cover(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Account not exist")

        return response

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(task_content)

    return response

@csrf_exempt
def get_child_tasks(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_task_manager = TaskManager()
    result, task_content = obj_task_manager.get_child_tasks(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Account not exist")

        return response

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "task":task_content}))

    return response

@csrf_exempt
def get_parent_task(request):
    # Get request
    req = request.POST.dict()

    # Get Project content
    obj_task_manager = TaskManager()
    result, task_content = obj_task_manager.get_parent_task(req)

    if result == False:
        response = HttpResponseBadRequest()
        response["Access-Control-Allow-Origin"] = "*"
        response.write("Account not exist")

        return response

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "task":task_content}))

    return response

@csrf_exempt
def send_project(request):
    # Get request
    req = request.POST.dict()

    # Send project
    result = send_gmail(req["title"], req["email"], req["content"])

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result}))

    return response

@csrf_exempt
def del_project(request):
    # Get request
    req = request.POST.dict()

    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.delete(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result}))

    return response

@csrf_exempt
def get_task_comment(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result, content = obj_task_manager.get_task_comment(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "comment":content}, ensure_ascii = False))

    return response

@csrf_exempt
def del_task(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result = "OK"
    result, content = obj_task_manager.delete(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result}))

    return response

@csrf_exempt
def verify_task(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result, content = obj_task_manager.verify_task(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}))

    return response

@csrf_exempt
def task_progress(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result, content = obj_task_manager.task_progress(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}))

    return response

@csrf_exempt
def get_task_weight(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result, content = obj_task_manager.weight(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

@csrf_exempt
def get_task_weight(request):
    # Get request
    req = request.POST.dict()

    obj_task_manager = TaskManager()
    result, content = obj_task_manager.weight(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def gps_set(request):
    # Get request
    req = request.POST.dict()

    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.gps_set(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def gps_get(request):
    # Get request
    req = request.POST.dict()

    obj_project_manager = ProjectManager()
    result, content = obj_project_manager.gps_get(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(content)

    return response

@csrf_exempt
def get_sroi(request):
    # Get request
    req = request.POST.dict()

    obj_SROI_manager = None
    content = None
    if ("uuid_project" in req):
      obj_SROI_manager = SROIManager(req)
      result, content = obj_SROI_manager.get_sroi(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(json.dumps(content, ensure_ascii = False))

    return response

@csrf_exempt
def get_sroi_meta(request):
    # Get request
    req = request.POST.dict()

    obj_SROI_manager = None
    content = None
    if ("uuid_project" in req):
      obj_SROI_manager = SROIManager(req)
      result, content = obj_SROI_manager.get_sroi_meta(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(json.dumps(content, ensure_ascii = False))

    return response

@csrf_exempt
def set_sroi(request):
    # Get request
    req = request.POST.dict()

    obj_SROI_manager = None
    content = None
    if ("uuid_project" in req):
      obj_SROI_manager = SROIManager(req)
      result, content = obj_SROI_manager.set_visible(req)

    # Response
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response.write(json.dumps(content, ensure_ascii = False))

    return response
