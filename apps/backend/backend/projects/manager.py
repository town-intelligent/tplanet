import datetime
import shutil
import os
from pathlib import Path, PurePath
import re
import ast
import json
import base64
import random
from pathlib import Path
from collections import defaultdict
from django.contrib.auth.models import User
from django.conf import settings
from distutils.util import strtobool

from .models import Task, Project, GPS
from projects.handler import set_task_content, year_txn_balance, set_task_weight

class ProjectManager:
    def __init__(self):
        pass

    def submit(self, req):
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        # TODO: Check task type
        if (obj_task.type_task == 1):
            obj_task = set_task_content(obj_task)
            dict_year_txn_balance = year_txn_balance(obj_task)
            return True, json.dumps(dict_year_txn_balance, ensure_ascii = False)
        elif (int(obj_task.type_task) == 0 or int(obj_task.type_task) == 3):
            # TODO
            set_task_weight(obj_task)
            return True, json.dumps(obj_task.weight, ensure_ascii = False)
        else:
            return True, json.dumps(obj_task.weight, ensure_ascii = False)

    def upload(self, req):
        obj_project = None

        # UUID
        try:
            obj_project = Project.objects.using("default").get(uuid = req["uuid"])
        except Exception as e:
            while True:
                obj_project = Project()
                n = 8
                uuid_project = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
                if not Project.objects.using("default").filter(uuid = uuid_project).exists():
                    obj_project.uuid = uuid_project
                    break

        # User
        obj_user = User.objects.using("default").get(email = req["email"])
        obj_project.obj_user = obj_user

        # Data
        req = defaultdict(lambda: None, req)

        try:
            if ("project_start_date" in req and "project_start_date" in req):
                obj_project.period = req["project_start_date"].replace(" ", "") + " - " + req["project_due_date"].replace(" ", "")
        except Exception as e:
            pass
        try:
            if ("name" in req):
                obj_project.name =  req["name"]
        except Exception as e:
            pass
        try:
            if ("business_philosophy" in req):
                obj_project.business_philosophy = req["business_philosophy"]
        except Exception as e:
            pass
        try:
            if ("list_project_type" in req):
                obj_project.project_type = req["list_project_type"]
        except Exception as e:
            pass
        try:
            if ("motivation" in req):
                obj_project.motivation = req["motivation"]
        except Exception as e:
            pass
        try:
            if ("project_planning" in req):
                obj_project.project_planning = req["project_planning"]
        except Exception as e:
            pass
        try:
            if ("list_sdg" in req):
                obj_project.weight = req["list_sdg"]
        except Exception as e:
            pass
        try:
            if ("list_sr" in req):
                obj_project.sr = req["list_sr"]
        except Exception as e:
            pass
        try:
            if ("hoster" in req):
                obj_project.hoster = req["hoster"]
        except Exception as e:
            pass
        try:
            if ("hoster_email" in req):
                obj_project.email = req["hoster_email"]
        except Exception as e:
            pass
        try:
            if ("org" in req):
                obj_project.org = req["org"]
        except Exception as e:
            pass
        try:
            if ("tel" in req):
                obj_project.tel = req["tel"]
        except Exception as e:
            pass
        try:
            if ("list_location" in req):
                obj_project.location = req["list_location"]
        except Exception as e:
            pass
        try:
            if ("budget" in req):
                obj_project.budget = req["budget"]
        except Exception as e:
            pass
        try:
            if ("relate_people" in req):
                obj_project.relate_people = req["relate_people"]
        except Exception as e:
            pass
        try:
            if ("project_a" in req):
                obj_project.project_a = req["project_a"]
        except Exception as e:
            pass
        try:
            if ("project_b" in req):
                obj_project.project_b = req["project_b"]
        except Exception as e:
            pass
        try:
            if ("philosophy" in req):
                obj_project.philosophy = req["philosophy"]
        except Exception as e:
            pass
        try:
            if ("weight_description" in req):
                obj_project.weight_description = req["weight_description"]
        except Exception as e:
            pass
        try:
            if ("status" in req):
                obj_project.status = req["status"]
        except Exception as e:
            obj_project.status = 0
            pass

        obj_project.save()

        return True, json.dumps({"uuid":obj_project.uuid}, ensure_ascii = False)

    def weight(self, uuid_task):
        if not Task.objects.using("default").filter(uuid = uuid_task).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = uuid_task)

        if obj_task.type_task == 1:
            dict_year_txn_balance = year_txn_balance(obj_task)
            return True, json.dumps(dict_year_txn_balance, ensure_ascii = False)

        queryset_tasks =  Task.objects.using("default").filter( obj_project = obj_task.obj_project)

        total_weight = {"sdgs-1": "0", "sdgs-2": "0", "sdgs-3": "0", "sdgs-4": "0", "sdgs-5": "0", "sdgs-6": "0", "sdgs-7": "0", "sdgs-8": "0", "sdgs-9": "0", "sdgs-10": "0", "sdgs-11": "0", "sdgs-12": "0", "sdgs-13": "0", "sdgs-14": "0", "sdgs-15": "0", "sdgs-16": "0", "sdgs-17": "0", "sdgs-18": "0", "sdgs-19": "0", "sdgs-20": "0","sdgs-21": "0", "sdgs-22": "0", "sdgs-23": "0", "sdgs-24": "0", "sdgs-25": "0", "sdgs-26": "0", "sdgs-27": "0"} 
        for obj in queryset_tasks:
            # Get task weight
            try:
                task_wight = json.loads(obj.weight)

                for index in range(27):
                    path = "sdgs-" + str(index + 1)
                    total_weight[path] = str(int(total_weight[path]) + int(task_wight[path]))
            except:
                pass

        return True, json.dumps(total_weight, ensure_ascii = False)

    def get(self, uuid_project):
        if not Project.objects.using("default").filter(uuid = uuid_project).exists():
            return False, "Project not exist"

        obj_project = Project.objects.using("default").get(uuid = uuid_project)

        # return True, obj_project.content
        dict_project = {"uuid":obj_project.uuid, "img":obj_project.img, 
                "project_a":obj_project.project_a, "project_b":obj_project.project_b,
                "name":obj_project.name, "philosophy":obj_project.philosophy,
                "period":obj_project.period, "budget":obj_project.budget, "relate_people":obj_project.relate_people,
                "project_type":obj_project.project_type, "motivation":obj_project.motivation, 
                "motivation_img":obj_project.motivation_img, "project_planning":obj_project.project_planning, 
                "project_planning_img":obj_project.project_planning_img,
                "weight":obj_project.weight, "weight_description":obj_project.weight_description,
                "sr":obj_project.sr, "hoster":obj_project.hoster, "email": obj_project.email,
                "org":obj_project.org, "tel":obj_project.tel, "location":obj_project.location,
                "status":obj_project.status}

        return True, json.dumps(dict_project, ensure_ascii = False)

    def delete(self, req):
        if not Project.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Project not exist"

        obj_project = Project.objects.using("default").get(uuid = req["uuid"])

        # Remove object
        obj_project.delete()

        # Remove static folder
        path_static_path = "backend/static/project/" + obj_project.uuid
        if (os.path.exists(path_static_path)):
            shutil.rmtree(path_static_path, ignore_errors = True)

        return True, json.dumps("OK", ensure_ascii = False)

    def list_tasks(self, req):
        if not Project.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Project not exist"

        object_project = Project.objects.using("default").get(uuid = req["uuid"])

        list_tasks = []

        # Get tasks queryset
        queryset_tasks = Task.objects.using("default").filter(obj_project = object_project)

        for obj in queryset_tasks:
            if(int(req["parent"]) == 1):
                if(obj.parent_task == None):
                    list_tasks.append(obj.uuid)
            else:
                list_tasks.append(obj.uuid)

        return True, json.dumps({"result":"true", "tasks":list_tasks}, ensure_ascii = False)

    def list_projects(self, req):
        list_projects = []

        # === 1️⃣ Email 過濾 ===
        if "email" in req and req["email"]:
            if not User.objects.using("default").filter(email=req["email"]).exists():
                print("Error, Account not exist - " + req["email"])
                return False, "Account not exist"

            object_user = User.objects.using("default").get(email=req["email"])
            queryset_projects = Project.objects.using("default").filter(
                obj_user=object_user, project_type="0"
            )
        else:
            queryset_projects = Project.objects.using("default").filter(project_type="0")

        # === 2️⃣ 收集所有 UUID ===
        list_projects = [obj.uuid for obj in queryset_projects]

        # === 3️⃣ SDG 過濾（若有傳入） ===
        if "sdg" in req and req["sdg"] != "":
            list_output = []
            for uuid in list_projects:
                try:
                    obj_project = Project.objects.using("default").get(uuid=uuid)
                    list_weight = obj_project.weight.split(",")
                    sdg_index = int(req["sdg"])
                    if (
                        len(list_weight) > sdg_index
                        and list_weight[sdg_index] == "1"
                    ):
                        list_output.append(uuid)
                except Exception:
                    pass
            list_projects = list_output

        # === 4️⃣ 分頁（可選） ===
        page = int(req.get("page", 0))
        page_size = int(req.get("page_size", 9))

        total_count = len(list_projects)
        total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 1

        if page > 0:
            start = (page - 1) * page_size
            end = start + page_size
            list_projects = list_projects[start:end]

            result = {
                "result": "true",
                "projects": list_projects,
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "total_pages": total_pages,
            }
        else:
            # 舊格式（完全不變）
            result = {"result": "true", "projects": list_projects}

        # === 5️⃣ 回傳 ===
        return True, json.dumps(result, ensure_ascii=False)

    def push_project_cover(self, req):
        # Get project queryset
        if not Project.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Project not exist"

        obj_project = Project.objects.using("default").get(uuid = req["uuid"])

        # Mkdir
        PATH_COVER = settings.STATICFILES_DIRS[0] + "/project/" + obj_project.uuid + "/media/cover"
        path_dir_cover = Path(PATH_COVER)
        path_dir_cover.mkdir(parents = True, exist_ok = True)

        # Save
        if ("jpeg" in req["img"]):
            req["img"] = req["img"].replace("data:image/jpeg;base64,", "")
        else:
            req["img"] = req["img"].replace("data:image/png;base64,", "")
        file_content = base64.b64decode(req["img"])
        with open(PATH_COVER + "/cover.png","wb") as f:
            f.write(file_content)

        obj_project.img = settings.STATIC_URL + "project/" + obj_project.uuid + "/media/cover/cover.png"
        obj_project.save()

        return True, json.dumps({"result":"true", "url":obj_project.img}, ensure_ascii = False)

    def gps_set(self, req):
        #if not Project.objects.using("default").filter(uuid = req["uuid_project"]).exists():
        #    return False, "Project not exist"
        #
        # obj_project = Project.objects.using("default").get(uuid = req["uuid_project"])
        
        # Set task
        if not Task.objects.using("default").filter(uuid = req["uuid_task"]).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid_task"])

        # Create project GPS model
        obj_gps = GPS()
        
        # Set project
        if Task.objects.using("default").filter(obj_project = obj_task.obj_project).exists():
            try:
                obj_gps.obj_project = obj_task.obj_project
            except Exception as e:
                print(e)
                pass

        obj_gps.obj_task = obj_task

        try:
            obj_user = User.objects.using("default").get(email = req["email"])
            obj_gps.obj_user = obj_user
        except:
            pass

        try:
            obj_gps.gps = req["lat"] + "," + req["lon"]
        except:
            pass

        obj_gps.save()

        return True, json.dumps("OK", ensure_ascii = False)

    def gps_get(self, req):
        if not Project.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Project not exist"

        obj_proj = Project.objects.using("default").get(uuid = req["uuid"])
       
        content = []
        if (GPS.objects.using("default").filter(obj_project = obj_proj).exists()):
            queryset_gps = GPS.objects.using("default").filter(obj_project = obj_proj)

            for obj in queryset_gps:
                value = {"gps":obj.gps, "uuid_task":obj.obj_task.uuid, "created_at":str(obj.created_at)}
                content.append(value)

        return True, json.dumps(content, ensure_ascii = False)

class TaskManager:
    def __init__(self):#, req_username):
        pass
        # Get user
        # obj_user = User.objects.using("default").get(username = req_username)

    def create_task(self, req):
        # Check project exist
        if not Project.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Project " + req["uuid"] + "not exist")
            return False, "Project not exist"

        obj_project = Project.objects.using("default").get(uuid =req["uuid"])

        # Get user
        obj_user = User.objects.using("default").get(email = req["email"])

        # Append tasks to project
        uuid_task = None
        obj_task = None

        if "task" in req:
            obj_task = Task.objects.using("default").get(uuid = req["task"])
        else:
            obj_task = Task()
            while True:
                n = 8
                uuid_task = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
                if not Task.objects.using("default").filter(uuid = uuid_task).exists():
                    obj_task.uuid = uuid_task
                    break

        obj_task.obj_user = obj_user
        obj_task.obj_project = obj_project

        # Content
        try:
            obj_task.token = req["token"]
        except Exception as e:
            print(e)
            obj_task.token = 0
            pass

        if "type" not in req:
            obj_task.type_task = 0
            obj_task.overview = "SDGS 永續問卷"
        else:
            obj_task.type_task = int(req["type"])
            # obj_task.overview = req["overview"]

        # Tasks
        try:
            # list_tasks = ast.literal_eval(re.sub(r'\b0+\B', '', req["tasks"]))
            list_tasks = ast.literal_eval(re.sub(r'', '', req["tasks"]))
            task_content = {"sdgs-1": "0", "sdgs-2": "0", "sdgs-3": "0", "sdgs-4": "0", "sdgs-5": "0", "sdgs-6": "0", "sdgs-7": "0", "sdgs-8": "0", "sdgs-9": "0", "sdgs-10": "0", "sdgs-11": "0", "sdgs-12": "0", "sdgs-13": "0", "sdgs-14": "0", "sdgs-15": "0", "sdgs-16": "0", "sdgs-17": "0", "sdgs-18": "0", "sdgs-19": "0", "sdgs-20": "0","sdgs-21": "0", "sdgs-22": "0", "sdgs-23": "0", "sdgs-24": "0", "sdgs-25": "0", "sdgs-26": "0", "sdgs-27": "0"}
            
            for obj in list_tasks:
                if ("task_parent_id" in obj):
                    # Set parent task to task
                    str_parent_task_id = obj["task_parent_id"]
                    if not Task.objects.using("default").filter(uuid = str_parent_task_id).exists():
                        print("Error, Parent task not exist " + str_parent_task_id)
                        return False, "Parent task not exist"
                    obj_parent_task = Task.objects.using("default").get(uuid = str_parent_task_id)
                    obj_task.parent_task = obj_parent_task
                else:
                    task_content["sdgs-" + str(int(obj["sdg"]))] = "1"#obj["des"]

            obj_task.content = json.dumps(task_content)
        except Exception as e:
            print(e)
            pass

        # Set name
        try:
            obj_task.name = req["name"]
        except Exception as e:
            print(e)
            pass

        # Set overview
        try:
            obj_task.overview = req["overview"]
        except Exception as e:
            print(e)
            pass

        # Set partent data
        try:
            obj_task.period = req["task_start_date"] + "-" + req["task_due_date"]
        except Exception as e:
            print(e)
            pass

        # Cover
        if "cover" in req:
            if "data:image/png;base64," in req["cover"]:
                req["cover"] = req["cover"].replace("data:image/png;base64,", "")
            else:
                req["cover"] = req["cover"].replace("data:image/jpeg;base64,", "")

            file_content = base64.b64decode(req["cover"])

            # Mkdir
            PATH_COVER = settings.STATICFILES_DIRS[0] + "/project/" + req["uuid"] + "/tasks/" + obj_task.uuid + "/cover"
            path_dir_cover = Path(PATH_COVER)
            path_dir_cover.mkdir(parents = True, exist_ok = True)

            # Save
            file_content = base64.b64decode(req["cover"])
            with open(PATH_COVER + "/cover.png","wb") as f:
                f.write(file_content)

            obj_task.thumbnail = settings.STATIC_URL + "project/" + obj_task.obj_project.uuid + "/tasks/" + obj_task.uuid + "/cover/cover.png"

        # GPS
        try:
            obj_task.gps_flag = bool(strtobool(req["gps_flag"]))
        except Exception as e:
            print(e)
            obj_task.gps_flag = False
            pass

        obj_task.save()

        return True, obj_task.uuid

    def get(self, uuid_task):
        if not Task.objects.using("default").filter(uuid = uuid_task).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = uuid_task)

        obj_content = ""
        obj_weight = ""
        try:
            obj_content = obj_task.content
            obj_weight = json.loads(obj_task.weight)
        except Exception as e:
            print("Error, except on task ID " + obj_task.uuid + " " + str(e))
            print("Error, obj_content = " + obj_content)
            print("Error, obj_weight = " + obj_weight)
            pass

        dict_task = {"uuid":obj_task.uuid, "name":obj_task.name, "type_task":obj_task.type_task,
                "thumbnail":obj_task.thumbnail, "content":obj_content, "overview":obj_task.overview, 
                "weight":obj_weight, "token":obj_task.token, "period":obj_task.period, "gps":obj_task.gps_flag}

        print(json.dumps(dict_task, ensure_ascii = False))
        return True, json.dumps(dict_task, ensure_ascii = False)

    def submit(self, request):
        if not Task.objects.using("default").filter(uuid = request["uuid"]).exists():
            return False, "Task not exist"

        # Get project weight
        obj_task = Task.objects.using("default").get(uuid = request["uuid"])
        obj_project = ProjectManager()

        result, weight_project = obj_project.submit(request)

        return True, json.dumps(json.loads(weight_project), ensure_ascii = False)

    def comment(self, request):
        result = {"status":"OK"}

        # Request valid check
        if not Task.objects.using("default").filter(uuid = request["uuid"]).exists():
            return False, "Task not exist"

        # Environment
        obj_task = Task.objects.using("default").get(uuid = request["uuid"])
        PATH_COMMENT = settings.STATICFILES_DIRS[0] + "/project/" + obj_task.obj_project.uuid + "/tasks/" + request["uuid"] + "/" + request["email"]
        path_dir_comment = Path(PATH_COMMENT)

        # Mkdir
        path_dir_comment.mkdir(parents = True, exist_ok = True)

        # Save comment
        file_comment = open(PATH_COMMENT + "/comment.txt", "w")
        file_comment.write(request["comment"])
        file_comment.close()

        # Save status
        PATH_STATUS = settings.STATICFILES_DIRS[0] + "/project/" + obj_task.obj_project.uuid + "/tasks/" + request["uuid"] + "/" + request["email"]
        file_status = open(PATH_STATUS + "/status.txt", "w+")
        file_status.write("0")
        file_status.close()

        # Save picture
        if "img" in request:
            try:
                if "data:image/png;base64," in request["img"]:
                    request["img"] = request["img"].replace("data:image/png;base64,", "")
                else:
                    request["img"] = request["img"].replace("data:image/jpeg;base64,", "")

                file_content = base64.b64decode(request["img"])

                path_dir_task_img = Path(PATH_COMMENT)

                with open(PATH_COMMENT + "/img.png","wb") as f:
                    f.write(file_content)
            except Exception as e:
                print(e)
                pass

        return True, json.dumps(result, ensure_ascii = False)

    def push_task_cover(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Task not exist")
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        # Save picture
        if "img" in req:
            if "data:image/png;base64," in req["img"]:
                req["img"] = req["img"].replace("data:image/png;base64,", "")
            else:
                req["img"] = req["img"].replace("data:image/jpeg;base64,", "")

            PATH_TASK_COVER = settings.STATICFILES_DIRS[0] + "/project/" + obj_task.obj_project.uuid + "/tasks/" + req["uuid"] + "/"

            path_dir_task_cover = Path(PATH_TASK_COVER)

            # Mkdir
            path_dir_task_cover.mkdir(parents = True, exist_ok = True)

            file_content = base64.b64decode(req["img"])
            with open(PATH_TASK_COVER + "/cover.png","wb") as f:
                f.write(file_content)

        obj_task.thumbnail = settings.STATIC_URL + "project/" + obj_task.obj_project.uuid + "/tasks/" + req["uuid"] + "/cover.png"
        obj_task.save()

        return True, json.dumps({"result":"true", "url":obj_task.thumbnail}, ensure_ascii = False)

    def get_child_tasks(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Task not exist")
            return False, "Task not exist"

        list_tasks = []
        obj_parent_task = Task.objects.using("default").filter(uuid = req["uuid"])
        queryset_tasks = Task.objects.using("default").filter(parent_task__in = obj_parent_task)

        for obj in queryset_tasks:
            list_tasks.append(obj.uuid)

        return True, list_tasks
 
    def get_parent_task(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Error, task not exist")
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        return True, obj_task.parent_task.uuid

    def get_task_comment(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Error, task not exist")
            return False, "Task not exist"

        # Get task object
        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        # Get task project uuid
        uuid_project = obj_task.obj_project.uuid

        # Get task comment folder path
        list_comments = []
        str_path = "backend/static/project/" + uuid_project + "/tasks/" + req["uuid"]
        for path in Path(str_path).iterdir():
            if not path.is_dir():
                continue

            # Get email
            str_email = PurePath(path).parts[-1]

            # Get status
            str_status = "0"
            path_status = Path(str_path + "/" + str_email + "/status.txt")
            if (os.path.exists(path_status)):
                str_status = Path(path_status).read_text()

            str_comment = Path(str_path + "/" + str_email + "/comment.txt").read_text()
            str_img = "/static/project/" + uuid_project + "/tasks/" + req["uuid"] + "/" + str_email + "/" + "img.png"

            obj_comment = {"email":str_email, "comment":str_comment, "img":str_img, "status":str_status}
            list_comments.append(obj_comment)

        return True, list_comments

    def delete(self, req):
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        # Remove object return True
        obj_task.delete()

        # Remove static folder
        path_static_path = "backend/static/project/" + obj_task.obj_project.uuid + "/tasks/" + obj_task.uuid
        if (os.path.exists(path_static_path)):
            shutil.rmtree(path_static_path, ignore_errors = True)

        return True, json.dumps("OK", ensure_ascii = False)

    def verify_task(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Error, task not exist")
            return False, "Task not exist"

        # Get task object
        obj_task = Task.objects.using("default").get(uuid = req["uuid"])

        # Get task project uuid
        uuid_project = obj_task.obj_project.uuid

        str_path = "backend/static/project/" + uuid_project + "/tasks/" + req["uuid"]
        for path in Path(str_path).iterdir():
            if not path.is_dir():
                continue

        # Comment status
        list_email = json.loads(req["listEmail"])
        for obj_email in list_email:
            str_path_comment = str_path + "/" + obj_email + "/status.txt"

            file_status = open(str_path_comment, 'w+')
            file_status.write("1")
            file_status.close()

        return True, "OK"

    def task_progress(self, req):
        # Request valid check
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            print("Error, task not exist")
            return False, "Task not exist"

        # Get task object
        obj_task = Task.objects.using("default").get(uuid = req["uuid"])
        obj_parent_task = None

        # Get parent task
        if (obj_task.parent_task != None):
            obj_parent_task = obj_task.parent_task
        else:
            obj_parent_task = obj_task

        # Get all child tasks
        list_child_tasks = []
        result = {"verified":"", "all":""}
        queryset_child_tasks = Task.objects.using("default").filter(parent_task = obj_parent_task)
        if (queryset_child_tasks.count() != 0):
            for obj_task in queryset_child_tasks:
                list_child_tasks.append(obj_task.uuid)

        # Get all verified tasks
        # Get task project uuid
        list_child_verified_tasks = []
        uuid_project = obj_task.obj_project.uuid

        if (queryset_child_tasks.count() != 0):
            for obj_task in queryset_child_tasks:
                path_status_path = "backend/static/project/" + uuid_project + "/tasks/" + obj_task.uuid + "/" + req["email"] + "/status.txt"
                if (os.path.exists(path_status_path)):
                    str_status = Path(path_status_path).read_text()
                    if (str_status == "1"):
                        list_child_verified_tasks.append(obj_task.uuid)

        # Final
        result["all"] = list_child_tasks
        result["verified"] = list_child_verified_tasks

        return True, result

    def weight(self, req):
        if not Task.objects.using("default").filter(uuid = req["uuid"]).exists():
            return False, "Task not exist"

        obj_parent_task = Task.objects.using("default").filter(uuid = req["uuid"])
        queryset_tasks = Task.objects.using("default").filter(parent_task__in = obj_parent_task)

        total_weight = {"sdgs-1": "0", "sdgs-2": "0", "sdgs-3": "0", "sdgs-4": "0", "sdgs-5": "0", "sdgs-6": "0", "sdgs-7": "0", "sdgs-8": "0", "sdgs-9": "0", "sdgs-10": "0", "sdgs-11": "0", "sdgs-12": "0", "sdgs-13": "0", "sdgs-14": "0", "sdgs-15": "0", "sdgs-16": "0", "sdgs-17": "0", "sdgs-18": "0", "sdgs-19": "0", "sdgs-20": "0","sdgs-21": "0", "sdgs-22": "0", "sdgs-23": "0", "sdgs-24": "0", "sdgs-25": "0", "sdgs-26": "0", "sdgs-27": "0"}

        for obj in queryset_tasks:
            # Get task weight
            try:
                task_wight = json.loads(obj.weight)

                for index in range(27):
                    path = "sdgs-" + str(index + 1)
                    total_weight[path] = str(int(total_weight[path]) + int(task_wight[path]))
            except:
                pass

        return True, json.dumps(total_weight, ensure_ascii = False)
