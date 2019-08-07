"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import webapp.providers.classified_widget as widgets
import json
import pandas as pd
from scipy.stats import linregress
from webapp.providers.helpers import line_to_percent

def get_anomaly_trend(line_data : pd.DataFrame) -> float:
    """
    takes data for a line and calculates the anomaly trend from it.
    """
    line_data = pd.DataFrame(line_data).sort_values("classified_time").reset_index(drop=True)
    line_data["time_linreg"] = line_data["classified_time"].map(lambda x: x.timestamp())
    slope, intercept, _, _, _ = linregress(line_data["time_linreg"].values, line_data["std_dist"])
    return line_to_percent(slope, intercept, line_data["time_linreg"].values)

def get_line_overviews(db_cnxn, factory_id):
    """
    gets the line overview from a single factory
    """
    cursor = db_cnxn.cursor()
    sql = "select * from dbo.classified_widgets where factory_id = '{}'".format(factory_id)
    data = []
    for row in cursor.execute(sql):
        res = {}
        res["classified_time"] = row.classified_time
        res["std_dist"] = row.std_dist
        res["line_id"] = row.line_id
        res["is_good"] = row.is_good
        data.append(res)
    data = pd.DataFrame(data)
    line_ids = data["line_id"].unique().tolist()
    line_datas = {}
    for line_id in line_ids:
        line_datas[line_id] = {}
        line_data = data[data["line_id"] == line_id]
        line_datas[line_id]["good_count"] = line_data[line_data["is_good"] == True]["is_good"].shape[0]
        line_datas[line_id]["bad_count"] = line_data[line_data["is_good"] == False]["is_good"].shape[0]
        line_datas[line_id]["perc_anomalies"] = line_datas[line_id]["bad_count"] / (line_datas[line_id]["good_count"] + line_datas[line_id]["bad_count"])
        line_datas[line_id]["anomaly_trend"] = get_anomaly_trend(line_data)
    return line_datas