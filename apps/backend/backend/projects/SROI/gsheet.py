import pygsheets
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .config import *

# 初始化 Google Drive 服務
def initialize_drive_service(credentials_file):
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=credentials)

    return drive_service

# 檢查檔案是否存在
def check_file_exists(service, file_id):
    try:
        file = service.files().get(fileId=file_id, fields='id').execute()
        return True
    except HttpError as error:
        if error.resp.status == 404:
            return False
        else:
            print("檢查檔案時發生錯誤：", error)
            return False

# 建立子資料夾
def create_sub_folder(service, parent_folder_id, sub_folder_name):
    try:
        folder_metadata = {
            'name': sub_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        new_folder = service.files().create(body=folder_metadata, fields='id').execute()
        return new_folder.get('id')
    except Exception as error:
        print("建立子資料夾時發生錯誤：", error)
        return None

# 複製檔案到資料夾
def copy_file_to_folder(service, file_id, folder_id, new_name, budget):
    try:
        new_file_metadata = {'name': new_name, 'parents': [folder_id]}
        new_file = service.files().copy(fileId=file_id, body=new_file_metadata).execute()

        # 設置新文件的權限，使得知道連結的人可以編輯
        new_file_id = new_file.get('id')
        new_permission = {
            'type': 'anyone',  # 表示任何知道連結的人
            'role': 'writer'   # 'writer' 表示可以編輯
        }

        service.permissions().create(
            fileId=new_file_id,
            body=new_permission
        ).execute()

        # Set Project budget
        gc = pygsheets.authorize(service_file=CREDENTIALS_FILE)
        # 開啟指定的工作表
        sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + new_file.get('id') + "/edit?usp=sharing")
        worksheet = sht.worksheet_by_title("總價值計算 (勿改)")
        worksheet.update_value("B5", int(budget))

        return new_file.get('id')

    except Exception as error:
        print("複製檔案時發生錯誤：", error)
        return None

def update_google_sheet(file_id, obj_project):
    gc = pygsheets.authorize(service_file=CREDENTIALS_FILE)
    sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + file_id + "/edit?usp=sharing")
    worksheet = sht.worksheet_by_title("總價值計算 (勿改)")
    print("hello, obj_project.budget = " + str(obj_project.budget))
    worksheet.update_value("B5", obj_project.budget)

    return sht

def get_google_sheet(sroi_file_id):
    gc = pygsheets.authorize(service_file=CREDENTIALS_FILE)
    # 開啟指定的工作表
    sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + sroi_file_id + "/edit?usp=sharing")

    return sht

def get_google_sheet_as_dataframe(sroi_file_id):
    # SROI_FIELD
    gc = pygsheets.authorize(service_file=CREDENTIALS_FILE)
    # 開啟指定的工作表
    sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/" + sroi_file_id + "/edit?usp=sharing")

    sheet_titles = [field["sheet_title"] for field in SROI_FIELDS]
    worksheets = sht.worksheets()

    list_dataframe = []
    for sheet in worksheets:
        if sheet.title in sheet_titles:
            sheet_data = sht.worksheet_by_title(sheet.title)
            df = sheet_data.get_as_df(has_header = False)
            df.name = sheet.title
            list_dataframe.append(df)

    return list_dataframe

def get_key_string_index(worksheet, col, string):
    # 搜尋指定字串在 Column-A 中的儲存格
    col_cells = worksheet.get_col(col)

    # 搜尋指定字串在 Column-A 中的儲存格，並取得位置
    found_cells = [index for index, cell in enumerate(col_cells) if string in cell]

    if found_cells:
        for index in found_cells:
            return index + 1
    else:
        return -1
