"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import webapp.providers.classified_widget as widgets
import json
import pandas as pd
from scipy.stats import linregress
from webapp.providers.helpers import line_to_percent

class FactoryOverview():
    factory_id = None
    total_widgets = None
    total_anomalies = None
    percent_anomalies = None
    anomaly_trend = None

    def to_dict(self):
        res = {}
        res["factory_id"] = self.factory_id
        res["total_widgets"] = self.total_widgets
        res["total_anomalies"] = self.total_anomalies
        res["percent_anomalies"] = self.percent_anomalies
        res["anomaly_trend"] = self.anomaly_trend
        return res
    
    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)

def get_basic_widget_stats(cnxn, factory_id):
    """
    Returns tuple for totalwidgetcount, totalanomalycount, percent_anomalies
    """
    cursor = cnxn.cursor()
    sql = "SELECT COUNT(*) AS count from dbo.classified_widgets where is_good = 0 and factory_id = '{}'".format(factory_id)
    bad_count = cursor.execute(sql).fetchone().count
    sql = "SELECT COUNT(*) AS count from dbo.classified_widgets where factory_id = '{}'".format(factory_id)
    total_count = cursor.execute(sql).fetchone().count
    percent_anomalies = bad_count / total_count
    return bad_count, total_count, percent_anomalies

def get_anomaly_trend(cnxn, factory_id):
    """
    Gets anomaly trend
    """
    cursor = cnxn.cursor()
    sql = "select * from dbo.classified_widgets where factory_id = '{}'".format(factory_id)
    data = []
    for row in cursor.execute(sql):
        res = {}
        res["classified_time"] = row.classified_time
        res["std_dist"] = row.std_dist
        data.append(res)
    data = pd.DataFrame(data).sort_values("classified_time").reset_index(drop=True)
    data["time_linreg"] = data["classified_time"].map(lambda x: x.timestamp())
    slope, intercept, _, _, _ = linregress(data["time_linreg"].values, data["std_dist"])
    return line_to_percent(slope, intercept, data["time_linreg"].values)

def get_factory_overview(db_cnxn, factory_id) -> dict:
    """
    returns jsonified FactoryOverview
    """
    overview = FactoryOverview()
    overview.factory_id = factory_id
    overview.total_anomalies, overview.total_widgets, overview.percent_anomalies = get_basic_widget_stats(db_cnxn, factory_id)
    overview.anomaly_trend = get_anomaly_trend(db_cnxn, factory_id)
    return overview.to_dict()

def get_all_overviews(db_cnxn, factories_list) -> str:
    f_overviews = []
    for factory in factories_list:
        data = get_factory_overview(db_cnxn, factory)
        f_overviews.append(data)
    return json.dumps(f_overviews)
