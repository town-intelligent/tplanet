import re
import pandas as pd
import pygsheets
from .gsheet import get_key_string_index

def append_field_data(selected_data, dict_sroi, field, index):
    for row in selected_data.iterrows():
        dict_sroi[field][index]["value"].append(list(row[1]))

    return True

def get_environment_data(df, dict_sroi):
    offset_flag = 2
    for index in range(len(dict_sroi["sroi_environment"])):
        offset_flag = 2
        # Start / end string
        end_string = "環境面向價值計算 (小計)"
        try:
            start_string = dict_sroi["sroi_environment"][index]["head"][0]
        except Exception as e:
            offset_flag = 1
            try:
                start_string = dict_sroi["sroi_environment"][index]["key"][0]
            except Exception as e:
                pass

        try:
            end_string = dict_sroi["sroi_environment"][index + 1]["head"][0]
        except Exception as e:
            try:
                end_string = dict_sroi["sroi_environment"][index + 1]["key"][0]
            except Exception as e:
                pass

        # Start / end index
        start_index = df[df[0].astype(str).str.contains(re.escape(start_string))].index
        end_index = df[df[0].astype(str).str.contains(re.escape(end_string))].index

        # Selected data
        selected_data = df.iloc[start_index[0] + offset_flag:end_index[0]]
        append_field_data(selected_data, dict_sroi, "sroi_environment", index)

    return True

def get_economy_data(df, dict_sroi):
    for index in range(len(dict_sroi["sroi_economy"])):
        # Start / end string
        start_string = dict_sroi["sroi_economy"][index]["head"][0]
        end_string = "經濟面向價值計算 (小計)"
        if index + 1 < len(dict_sroi["sroi_economy"]):
            end_string = dict_sroi["sroi_economy"][index + 1]["head"][0]

        # Start / end index
        start_index = df[df[0].astype(str).str.contains(re.escape(start_string))].index
        end_index = df[df[0].astype(str).str.contains(re.escape(end_string))].index

        # Selected data
        selected_data = df.iloc[start_index[0] + 2:end_index[0]]
        append_field_data(selected_data, dict_sroi, "sroi_economy", index)

    return True

def get_social_data(df, dict_sroi):
    for index in range(len(dict_sroi["sroi_social"])):
        # Start / end string
        start_string = dict_sroi["sroi_social"][index]["head"][0]
        end_string = "社會面向價值計算 (小計)"
        if index + 1 < len(dict_sroi["sroi_social"]):
            end_string = dict_sroi["sroi_social"][index + 1]["head"][0]

        # Start / end index
        start_index = df[df[0].astype(str).str.contains(re.escape(start_string))].index
        end_index = df[df[0].astype(str).str.contains(re.escape(end_string))].index

        # Selected data
        selected_data = df.iloc[start_index[0] + 2:end_index[0]]
        append_field_data(selected_data, dict_sroi, "sroi_social", index)

    return True

def total_value_calculation(list_df_sroi, dict_sroi):
    # 總價值計算
    cell_value = 0
    cell_location = None
    row = None

    # Get 總價值計算
    total_value_df = None
    for obj_df in list_df_sroi:
        if (obj_df.name == "總價值計算 (勿改)"):
            total_value_df = obj_df
            break

    # 總社會現值 (total_benefit) /
    # 社會面向價值計算 (小計) (social_subtotal) /
    # 經濟面向價值計算 (小計) (economy_subtotal) /
    # 環境面向價值計算 (小計) (environment_subtotal) /
    # 總投入價值 (total_cost) /
    # SROI (sroi)
    if (float(total_value_df.loc[1, 2]) > 0.0):
        dict_sroi["social_subtotal"] = float(total_value_df.loc[1, 2])
    if (float(total_value_df.loc[2, 2]) > 0.0):
        dict_sroi["economy_subtotal"] = float(total_value_df.loc[2, 2])
    if (float(total_value_df.loc[3, 2]) > 0.0):
        dict_sroi["environment_subtotal"] = float(total_value_df.loc[3, 2])
    if (float(total_value_df.loc[0, 1]) > 0.0):
        dict_sroi["total_benefit"] = float(total_value_df.loc[0, 1])
    if (float(total_value_df.loc[4, 1]) > 0.0):
        dict_sroi["total_cost"] = float(total_value_df.loc[4, 1])
    if (float(total_value_df.loc[5, 1]) > 0.0):
        dict_sroi["sroi"] = float(total_value_df.loc[5, 1])

    # 根據總價值計算爬取資料
    if (float(dict_sroi["social_subtotal"])) > 0.0:
        get_social_data([df for df in list_df_sroi if df.name == "社會面向 (S)"][0], dict_sroi)
    if (float(dict_sroi["economy_subtotal"])) > 0.0:
        get_economy_data([df for df in list_df_sroi if df.name == "經濟面向 (E)"][0], dict_sroi)
    if (float(dict_sroi["environment_subtotal"])) > 0.0:
        get_environment_data([df for df in list_df_sroi if df.name == "環境面向 (E)"][0], dict_sroi)

    return True