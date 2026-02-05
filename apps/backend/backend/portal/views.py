import os
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

from .manager import comment, comment_list, comment_delete, comment_get
from .manager import mockup_modify, mockup_fetch
from .manager import news_post_create, news_post_list, news_post_get, news_post_delete

@csrf_exempt
def get_comment(request):
    # Get request
    req = request.POST.dict()

    # Save
    result, content = comment_get(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}, ensure_ascii = False))
    
    return response

@csrf_exempt
def delete_comment(request):
    # Get request
    req = request.POST.dict()

    # Save
    result, content = comment_delete(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}, ensure_ascii = False))
    
    return response

@csrf_exempt
def list_comment(request):
    # Get request
    req = request.POST.dict()

    # Save
    result, content = comment_list(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}, ensure_ascii = False))
    
    return response

@csrf_exempt
def submit_comment(request):
    # Get request
    req = request.POST.dict()

    # Save
    result, uuid = comment(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "uuid":uuid}))
    
    return response

@csrf_exempt
def mockup_new(request):
    # API
    result, description = mockup_modify(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "description": description}))

    return response

@csrf_exempt
def mockup_get(request):
    # API
    result, description = mockup_fetch(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "description": description}))

    return response

@csrf_exempt
def news_create(request):
    # API
    result, content = news_post_create(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content": content}))

    return response

@csrf_exempt
def news_list(request):
    # API
    result, content = news_post_list(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content": content}))

    return response

@csrf_exempt
def news_get(request):
    # API
    result, content = news_post_get(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content": content}))

    return response

@csrf_exempt
def news_delete(request):
    # API
    result, content = news_post_delete(request)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content": content}))

    return response

@csrf_exempt
def upload_img(request):
    # Get request
    req = request.POST.dict()

    try:
      PATH_IMG_UPLOAD = settings.STATICFILES_DIRS[0] + "/media/imgs/"
      for filename, file in request.FILES.items():
          print(filename)
          # Save files
          f = open(PATH_IMG_UPLOAD + filename + os.path.splitext(file.name)[-1], "wb")
          f.write(file.read())
          f.close()

    except Exception as e:
      print(e)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":"OK"}))

    return response
