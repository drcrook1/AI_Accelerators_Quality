"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

def get_widget(db_cnxn, serial_number : str = None, db_id : str = None):
    cursor = db_cnxn.cursor()
    row = cursor.execute("select * from dbo.classified_widgets").fetchone()
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
