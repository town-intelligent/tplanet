import json
from datetime import datetime

from projects.models import Task

def set_task_weight(obj_task):
    if (obj_task.content == ""):
        return obj_task

    obj_weight = None
    if (obj_task.weight == ""):
        obj_weight = {"sdgs-1": "0", "sdgs-2": "0", "sdgs-3": "0", "sdgs-4": "0", "sdgs-5": "0", "sdgs-6": "0", "sdgs-7": "0", "sdgs-8": "0", "sdgs-9": "0", "sdgs-10": "0", "sdgs-11": "0", "sdgs-12": "0", "sdgs-13": "0", "sdgs-14": "0", "sdgs-15": "0", "sdgs-16": "0", "sdgs-17": "0", "sdgs-18": "0", "sdgs-19": "0", "sdgs-20": "0","sdgs-21": "0", "sdgs-22": "0", "sdgs-23": "0", "sdgs-24": "0", "sdgs-25": "0", "sdgs-26": "0", "sdgs-27": "0"}
    else:
        obj_weight = json.loads(obj_task.weight)

    obj_content = json.loads(obj_task.content)

    for key in obj_content:
        obj_weight[key] = str(int(obj_weight[key]) + int(obj_content[key]))

    obj_task.weight = json.dumps(obj_weight)
    obj_task.save()

    return obj_task


def set_task_content(obj_task):
    # Get current month
    current_month = datetime.now().month

    # Set content
    obj_content = None

    try:
        obj_content = json.loads(obj_task.content)
    except Exception as e:
        pass

    if obj_task.type_task == 1:
        obj_content[str(current_month)] = obj_content[str(current_month)] + obj_task.token
        obj_task.content = json.dumps(obj_content)
    else:
        # TODO: Add content
        # for key in task_content:
        #     project_weight[key] = project_weight[key] + task_content[key]
        pass

    obj_task.save()

    return obj_task

def year_txn_balance(obj_task):
    list_weight = []
    project_weight = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0, "12":0}

    # Get all tasks with project
    queryset_tasks =  Task.objects.using("default").filter( obj_project = obj_task.obj_project)

    for obj in queryset_tasks:
        # Get task content
        task_content = None
        try:
            task_content = json.loads(obj.content)
        except Exception as e:
            continue
        
        # Project
        for key in task_content:
            project_weight[key] = project_weight[key] + task_content[key]

            obj_weight = {}
            obj_weight["month"] = key
            obj_weight["value"] = project_weight[key]
            list_weight.append(obj_weight)

    return list_weight
