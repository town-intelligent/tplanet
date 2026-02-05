import copy
import os
import json
import pygsheets
from distutils.util import strtobool
from projects.models import SROI, Project
from .gsheet import initialize_drive_service, check_file_exists, create_sub_folder, copy_file_to_folder, get_google_sheet, get_google_sheet_as_dataframe, update_google_sheet
from .field import total_value_calculation, total_value_calculation
from .config import *

class SROIManager:
    def __init__(self, req):
        self.uuid_project = req["uuid_project"]
        self.drive_service = initialize_drive_service(CREDENTIALS_FILE)
        self.sroi_file_id = None
        self.visible = False
        self.uuid_project = None
        self.budget_project = 0

        # Check SROI Model exist
        if not Project.objects.using("default").filter(uuid = req["uuid_project"]).exists():
            return None

        obj_project = Project.objects.using("default").get(uuid = req["uuid_project"])
        self.budget_project = obj_project.budget
        self.uuid_project = req["uuid_project"]

        try:
          if not SROI.objects.using("default").filter(obj_project = obj_project).exists():
              folder_project_id = create_sub_folder(self.drive_service, PATH_ID_TARGET, req["uuid_project"])
              file_id = copy_file_to_folder(self.drive_service, FILE_ID_TO_COPY, folder_project_id, "SROI", self.budget_project)
              self.sroi_file_id = file_id
              obj_sroi = SROI()
              obj_sroi.obj_project = obj_project
              obj_sroi.visible = self.visible
              obj_sroi.file_id = file_id
              obj_sroi.save()
              return None
          else:
              obj_sroi = SROI.objects.using("default").get(obj_project = obj_project)
              self.sroi_file_id = obj_sroi.file_id
              return None
        except Exception as e:
            return None

    def get_sroi(self, req):
        # Check SROI Model exist
        if not Project.objects.using("default").filter(uuid = req["uuid_project"]).exists():
            return False, {"message":"Project not found"}

        obj_project = Project.objects.using("default").get(uuid = req["uuid_project"])

        if not SROI.objects.using("default").filter(obj_project = obj_project).exists():
            return False, {"message":"SROI not found"}

        obj_sroi = SROI.objects.using("default").get(obj_project = obj_project)

        # SROI basic information
        dict_sroi = copy.deepcopy(dict_sroi_init)

        dict_sroi["visible"] = obj_sroi.visible
        dict_sroi["file_id"] = self.sroi_file_id
        google_sht = get_google_sheet(self.sroi_file_id)

        # Update field
        google_sht = update_google_sheet(self.sroi_file_id, obj_project)

        # Convert Google sheet & calculate SROI
        list_df_sroi = get_google_sheet_as_dataframe(self.sroi_file_id)
        total_value_calculation(list_df_sroi, dict_sroi)

        return True, dict_sroi

    def get_sroi_meta(self, req):
        # Check SROI Model exist
        if not Project.objects.using("default").filter(uuid = req["uuid_project"]).exists():
            return False, {"message":"Project not found"}

        obj_project = Project.objects.using("default").get(uuid = req["uuid_project"])

        if not SROI.objects.using("default").filter(obj_project = obj_project).exists():
            return False, {"message":"SROI not found"}

        obj_sroi = SROI.objects.using("default").get(obj_project = obj_project)

        # Update field
        google_sht = update_google_sheet(obj_sroi.file_id, obj_project)

        # SROI basic information
        dict_sroi = {"uuid": req["uuid_project"], "file_id":"", "visible": obj_sroi.visible}
        dict_sroi["file_id"] = obj_sroi.file_id

        return True, dict_sroi

    def set_visible(self, req):
        try:
          obj_project = Project.objects.using("default").get(uuid = self.uuid_project)
          obj_sroi = SROI.objects.using("default").get(obj_project = obj_project)
          obj_sroi.visible = bool(strtobool(req["visible"]))
          obj_sroi.save()
          return True, {"visible":obj_sroi.visible, "file_id":obj_sroi.file_id}
        except Exception as e:
            return False, {"message":str(e)}
