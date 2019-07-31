"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from typing import List

def widget_from_row(row) -> Widget:
    w_class = Widget_Classification()
    w_class.classified_time = row.classified_time
    w_class.is_good = row.is_good
    w_class.threshold = row.threshold
    w_class.mean = row.mean
    w_class.std = row.std
    w_class.std_dist = row.std_dist

    wid = Widget()
    wid.classification = w_class
    wid.serial_number = row.serial_number
    wid.line_id = row.line_id
    wid.factory_id = row.factory_id
    return wid


def get_widget(db_cnxn, serial_number : str = None, db_id : str = None) -> Widget:
    cursor = db_cnxn.cursor()
    if(serial_number is not None):
        row = cursor.execute("select * from dbo.classified_widgets where serial_number = {}".format("'" + serial_number + "'")).fetchone()
    elif(db_id is not None):
        row = cursor.execute("select * from dbo.classified_widgets where id = {}".format("'" + db_id + "'")).fetchone()
    return widget_from_row(row)

def get_all_widgets(db_cnxn) -> List[Widget]:
    cursor = db_cnxn.cursor()
    widgets = []
    for row in cursor.execute("select * from dbo.classified_widgets"):
        widgets.append(widget_from_row(row))
    return widgets

def many_widgets_to_json(widgets : List[Widget]) -> str:
    """
    converts a list of widget objects to json
    """
    js_widgets = []
    for widget in widgets:
        js_widgets.append(widget.to_json())
    return js_widgets

def get_bad_widgets(db_cnxn, to_json : bool = False) -> List[Widget]:
    cursor = db_cnxn.cursor()
    widgets = []
    for row in cursor.execute("select * from dbo.classified_widgets where is_good = 0"):
        widgets.append(widget_from_row(row))
    if(to_json):
        return many_widgets_to_json(widgets)
    return widgets