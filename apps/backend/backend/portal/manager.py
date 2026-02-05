import shutil
import os
import json
import random
from pathlib import Path#, PurePath
from django.contrib.auth.models import User
from django.conf import settings

from .models import Comment
from .models import News

def comment_get(req):
    if not Comment.objects.using("default").filter(uuid = req["uuid"]).exists():
        return False, "Object not exist"

    obj_comment = Comment.objects.using("default").get(uuid = req["uuid"])
    content = {}

    try:
      content = {"uuid":obj_comment.uuid, "name":obj_comment.name, "email":obj_comment.email, \
            "org":obj_comment.org, "website":obj_comment.website, "tel":obj_comment.tel, \
            "comment":obj_comment.comment, "sdgs":json.loads(obj_comment.sdgs)}
    except:
        return False, "Error on handle comment"


    return True, content

def comment_delete(req):
    if not Comment.objects.using("default").filter(uuid = req["uuid"]).exists():
        return False, "Object not exist"

    obj_comment = Comment.objects.using("default").get(uuid = req["uuid"])

    # Remove object
    obj_comment.delete()
    
    return True, "OK"

def comment_list(req):
    if not User.objects.using("default").filter(email = req["owner"]).exists():
        print("Error, Account not exist - " + req["owner"])
        return False, "Account not exist"
    
    object_user = User.objects.using("default").get(email = req["owner"])

    content = []
    queryset_comment = Comment.objects.using("default").filter(obj_user = object_user)
    for obj_comment in queryset_comment:
        obj = {"uuid":obj_comment.uuid, "name":obj_comment.name, "email":obj_comment.email, \
                "org":obj_comment.org, "website":obj_comment.website, "tel":obj_comment.tel, \
                "comment":obj_comment.comment}
        content.append(obj)

    return True, content

def comment(req):
    obj_user = User.objects.using("default").get(email = req["owner"])

    obj_comment = Comment()
    obj_comment.obj_user = obj_user

    while True:
        n = 8
        uuid_comment = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
        if not Comment.objects.using("default").filter(uuid = uuid_comment).exists():
            obj_comment.uuid = uuid_comment
            break

    obj_comment.name = req["name"]
    obj_comment.email = req["email"]
    obj_comment.org = req["org"]
    obj_comment.website = req["website"]
    obj_comment.tel = req["tel"]
    obj_comment.comment = req["comment"]
    obj_comment.sdgs = req["list_target_sdgs"]

    obj_comment.save()

    return True, obj_comment.uuid

def mockup_modify(req):
    # Initial data
    PATH_MOCKUP = settings.STATICFILES_DIRS[0] + "/new_mockup/" + req.POST["email"]
    static_url = settings.STATIC_URL + "new_mockup/" + req.POST["email"] + "/"

    # Load old data
    old_des = None
    if os.path.exists(PATH_MOCKUP + "/description.json"):
        file_description = open(PATH_MOCKUP + "/description.json", "r")
        old_des = json.load(file_description)
        file_description.close()

    # Check mockup dir
    path_dir_mockup = Path(PATH_MOCKUP)
    path_dir_mockup.mkdir(parents = True, exist_ok = True)

    # Create index
    file_index = open(PATH_MOCKUP + "/index.html", "w")
    file_index.write("")
    file_index.close()

    # Create description
    raw_description = None
    description = {}
    try:
        raw_description = req.POST.dict()
    except:
        pass

    # Remove undefined and node items
    if (raw_description != None):
        for key, value in raw_description.items():
            if (raw_description[key] != "undefined" and raw_description[key] != None):
                description[key] = value

    # Save all static files
    for filename, file in req.FILES.items():
        # Save files
        f = open(PATH_MOCKUP + "/" + filename + os.path.splitext(file.name)[-1], "wb")
        f.write(file.read())
        f.close()

        # Update description
        description[filename] = static_url + filename + os.path.splitext(req.FILES[filename].name )[-1]

    # Update description - load original
    original_description = {}
    if os.path.exists(PATH_MOCKUP + "/description.json"):
        file_original_description = open(PATH_MOCKUP + "/description.json", "r")
        original_description = file_original_description.read()
        file_original_description.close()

        try:
            original_description = json.loads(original_description)
        except Exception as e:
            print(e)
            pass

    # Update description
    if (original_description != None and description !=None):
        for key in description:
            original_description[key] = description[key]

    # Write back
    file_description = open(PATH_MOCKUP + "/description.json", "w")
    file_description.write(json.dumps(original_description))
    file_description.close()

    return True, original_description

def mockup_fetch(req):
    # Check mockup dir
    PATH_MOCKUP = settings.STATICFILES_DIRS[0] + "/new_mockup/" + req.POST["email"]

    # Create description
    try:
        file_description = open(PATH_MOCKUP + "/description.json", "r")
        description = json.load(file_description)
        file_description.close()
    except:
        return True, {}

    return True, description

def news_post_create(req):
    req_dict = req.POST.dict()

    # Check owner exist
    if not User.objects.using("default").filter(email = req_dict["email"]).exists():
        print("Error, Account not exist - " + req_dict["email"])
        return False, "Account not exist"

    object_user = User.objects.using("default").get(email = req_dict["email"])

    # Variable
    content = {"banner":"", "img_0":"", "img_1":"", "img_2":""}
    obj_news = News()

    # UUID
    while True:
        n = 8
        uuid_news = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
        if not News.objects.using("default").filter(uuid = uuid_news).exists():
            obj_news.uuid = uuid_news
            break

    # Create news
    obj_news.obj_user = object_user
    obj_news.title = req_dict["title"]

    try:
        obj_news.description = req_dict["description"]
    except:
        pass

    try:
        if ("news_start" in req_dict and "news_end" in req_dict):
            obj_news.period = req_dict["news_start"].replace(" ", "") + " - " + req_dict["news_end"].replace(" ", "")
    except Exception as e:
        pass

    # Static file
    PATH_NEWS = settings.STATICFILES_DIRS[0] + "/news/" + obj_news.uuid
    try:
        path_dir_news = Path(PATH_NEWS)
        path_dir_news.mkdir(parents = True, exist_ok = True)

        f = open(PATH_NEWS + "/banner" +  os.path.splitext(req.FILES["banner"].name)[-1], "wb")
        f.write(req.FILES["banner"].read())
        f.close()
    except:
        pass

    try:
        for index in range(0, 3):
            f = open(PATH_NEWS + "/img_" + str(index) +  os.path.splitext(req.FILES["img_" + str(index)].name)[-1], "wb")
            f.write(req.FILES["img_" + str(index)].read())
            f.close()
    except:
        pass

    try:
        # Set response content
        static_url = settings.STATIC_URL + "news/" + obj_news.uuid + "/"
        # content["uuid"] = obj_news.uuid
        content["banner"]  = static_url + "banner" + os.path.splitext(req.FILES["banner"].name )[-1]
    except:
        pass

    try:
        for index in range(0, 3):
            content["img_" + str(index)]  = static_url + "img_" + str(index) +  os.path.splitext(req.FILES["img_" + str(index)].name)[-1]
    except:
        pass

    # Static in model
    obj_news.static = json.dumps(content)

    # Save
    obj_news.save()

    return True, content

def news_post_list(req):
    req_dict = req.POST.dict()

    # Check owner exist
    if not User.objects.using("default").filter(email = req_dict["email"]).exists():
        print("Error, Account not exist - " + req_dict["email"])
        return False, "Account not exist"

    object_user = User.objects.using("default").get(email = req_dict["email"])

    # Variable
    content = []

    if News.objects.using("default").filter(obj_user = object_user).exists():
         queryset_news = News.objects.using("default").filter(obj_user = object_user)
         for obj_news in queryset_news:
             content.append(obj_news.uuid)

    return True, content

def news_post_get(request):
    # Request data
    req = request.GET.dict()

    # Get news object
    if not News.objects.using("default").filter(uuid = req["uuid"]).exists():
        False, "News not exist"

    obj_news = News.objects.using("default").get(uuid = req["uuid"])

    # Static URL
    content = {"uuid":obj_news.uuid, "title":obj_news.title, "description":obj_news.description, "period":obj_news.period, "static":""}
    content["static"] = json.loads(obj_news.static)

    return True, content

def news_post_delete(req):
    req_dict = req.POST.dict()

    # Check owner exist
    if not User.objects.using("default").filter(email = req_dict["email"]).exists():
        print("Error, Account not exist - " + req_dict["email"])
        return False, "Account not exist"

    object_user = User.objects.using("default").get(email = req_dict["email"])

    # Variable
    content = []

    # Get news object
    if not News.objects.using("default").filter(uuid = req_dict["uuid"]).exists():
        False, "News not exist"

    obj_news = News.objects.using("default").get(uuid = req_dict["uuid"])

    # Remove object
    obj_news.delete()

    # Remove static folder
    path_static_path = "backend/static/news/" + obj_news.uuid
    if (os.path.exists(path_static_path)):
       shutil.rmtree(path_static_path, ignore_errors = True)

    return True, "OK"
