"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import webapp.providers.classified_widget as widgets
import json
import pandas as pd
from scipy.stats import linregress
from webapp.providers.helpers import line_to_percent
import math
from typing import List

def get_anomaly_trend(line_data : pd.DataFrame) -> float:
    """
    takes data for a line and calculates the anomaly trend from it.
    """
    line_data = pd.DataFrame(line_data).sort_values("classified_time").reset_index(drop=True)
    line_data["time_linreg"] = line_data["classified_time"].map(lambda x: x.timestamp())
    slope, intercept, _, _, _ = linregress(line_data["time_linreg"].values, line_data["std_dist"])
    perc = line_to_percent(slope, intercept, line_data["time_linreg"].values)
    if(math.isnan(perc)):
        perc = 0
    return perc

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
    line_datas = []
    for line_id in line_ids:
        result = {}
        line_data = data[data["line_id"] == line_id]
        result["good_count"] = line_data[line_data["is_good"] == True]["is_good"].shape[0]
        result["bad_count"] = line_data[line_data["is_good"] == False]["is_good"].shape[0]
        result["perc_anomalies"] = result["bad_count"] / (result["good_count"] + result["bad_count"])
        result["anomaly_trend"] = get_anomaly_trend(line_data)
        result["line_id"] = line_id
        line_datas.append(result)
    return line_datas

def get_factories_list(db_cnxn) -> List[str]:
    """
    gets distinct factories
    """
    cursor = db_cnxn.cursor()
    sql = "select distinct factory_id from dbo.classified_widgets"
    data = []
    for row in cursor.execute(sql):
        data.append(row.factory_id)
    return data

def get_all_overviews(db_cnxn, as_json = False):
    """
    creates a list of lists for all factories and lines in them.
    """
    overviews = []
    factory_id_list = get_factories_list(db_cnxn)
    for f_id in factory_id_list:
        result = {}
        result["factory_id"] = f_id
        result["line_overviews"] = get_line_overviews(db_cnxn, f_id)
        overviews.append(result)
    if(as_json):
        return json.dumps(overviews)
    return overviews