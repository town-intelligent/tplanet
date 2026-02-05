import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from accounts.avatar import Avatar

@csrf_exempt
def sign_up(request):
    # Get request
    req = request.POST.dict()

    # signup
    class_user = Avatar()
    result, jwt_token = class_user.signup(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"token":str(jwt_token)}))
    
    return response

@csrf_exempt
def sign_in(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    # result, jwt_token = class_user.signin(request.body)
    result, username, jwt_token = class_user.signin(req)

    # Signin_in fail
    if jwt_token == 403:
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response.status_code = 403
        response.write(json.dumps({"token":str(jwt_token)}))
        return response


    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"token":str(jwt_token), "username":username}))

    return response

@csrf_exempt
def verify_jwt(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, jwt_token = class_user.verify_jwt("admin", req["token"])

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "token":str(jwt_token)}))

    return response

@csrf_exempt
def forgot_password(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, content = class_user.forgot_password(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}))

    return response

@csrf_exempt
def get_group(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    group = class_user.get_group(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"group":group}))

    return response

@csrf_exempt
def set_group(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    group = class_user.set_group(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"group":group}))

    return response

@csrf_exempt
def google_login(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, username, jwt_token = class_user.oauth_google(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"token":str(jwt_token), "username":username}))

    return response

@csrf_exempt
def list_accounts(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, list_accounts = class_user.list_accounts(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "accounts":list_accounts}))

    return response


@csrf_exempt
def delete(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, content = class_user.delete(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"result":result, "content":content}))

    return response

@csrf_exempt
def google_login(request):
    # Get request
    req = request.POST.dict()

    # Get user
    class_user = Avatar()
    result, username, jwt_token = class_user.oauth_google(req)

    # Response
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps({"token":str(jwt_token), "username":username}))

    return response
