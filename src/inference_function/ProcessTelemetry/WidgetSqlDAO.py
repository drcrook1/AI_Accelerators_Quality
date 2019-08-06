import logging

from ai_acc_quality.data_models.widget import Widget

class WidgetSqlDAO:

    conn = None

    def __init__(self, connectFunction):
        self.connectFunction = connectFunction

    def connectODBC(self):
        if not self.conn:
            logging.info('Establishing ODBC connection')
            self.conn = self.connectFunction()
        return self.conn

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def persistWidget(self, w:Widget, id:str):
        conn = self.connectODBC()
        cur = conn.cursor()
        c = w.classification
        query = """INSERT INTO [dbo].[classified_widgets](
[serial_number], [std_dist], [std], [mean],
[threshold], [is_good], [id],
[factory_id], [line_id], [classified_time])
VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            w.serial_number, c.std_dist, c.std, c.mean,
            c.threshold, c.is_good()[1], id,
            w.factory_id, w.line_id, c.classified_time.isoformat(),)
        cur.execute(query, values)
        cur.commit()
        cur.close()


