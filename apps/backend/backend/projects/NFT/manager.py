import json
import requests

from django.conf import settings
from projects.models import Project, Task, NFT

class NFTManager:
    def __init__(self, req):
        # self.uuid_project = req["uuid_project"]
        pass
    def create_nft(self, req):
        headers = {"Content-Type": "application/json"}
        req_data = {"uuid_project": req["uuid_project"], "uuid_task": req["uuid_task"],"address":req["address"], "contract":req["contract"],\
        "callback":req["callback"], "description":req["description"], "name":req["name"], \
        "image":req["image"], "attributes":json.loads(req["attributes"])}
        r = requests.post(settings.NFT_API_ENDPOINT + "/mint", data=json.dumps(req_data), headers=headers)

        if (r.status_code != requests.codes.ok):
            print("NFT create fail")
            return False, "NFT create fail"

        return True, "OK"

    def set_token_id(self, req):
        if not Project.objects.using("default").filter(uuid = req["uuid_project"]).exists():
            return False, "Project not exist"

        obj_project = Project.objects.using("default").get(uuid = req["uuid_project"])

        if not Task.objects.using("default").filter(uuid = req["uuid_task"]).exists():
            return False, "Task not exist"

        obj_task = Task.objects.using("default").get(uuid = req["uuid_task"])

        if NFT.objects.using("default").filter(obj_task = obj_task).exists():
            return False, "NFT already exist"

        # Callback from minter
        try:
            obj_nft = NFT()
            obj_nft.obj_project = obj_project
            obj_nft.txn = settings.URL_OPENSEA + req["tokenid"]
            obj_nft.obj_task = obj_task
            obj_nft.save()
        except Exception as e:
            return False, str(e)

        return True, "OK"

    def set_nft_attr(self, req):
        # Get meta data
        r = requests.get(settings.NFT_API_ENDPOINT + "/uri/ning?id=" + req["tokenid"])

        if (r.status_code != requests.codes.ok):
            return False, "Get URI data fail"

        # Update meta data
        obj_original_metadata = None
        obj_new_attr = None

        try:
            obj_original_metadata = json.loads(r.text)
            obj_new_attr = json.loads(req["attributes"])
        except Exception as e:
            return False, str(e)

        obj_original_metadata["attributes"] = obj_new_attr

        # Submit meta data
        headers = {"Content-Type": "application/json"}
        data = json.dumps(obj_original_metadata, ensure_ascii=False).encode('utf-8')
        r = requests.post(settings.NFT_API_ENDPOINT + "/upload_meta_data", data=data, headers=headers)

        if (r.status_code != requests.codes.ok):
            return False, "NFT metadata update fail"

        return True, "OK"
