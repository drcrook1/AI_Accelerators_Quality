import logging

from ai_acc_quality.data_models.widget import Widget
from azure.storage.table import TableService
from datetime import timezone

class WidgetTableDAO:

    conn = None

    def __init__(self, tableService:TableService, tableName:str, maxTelemetriesPerRow:int=100):
        self.tableService = tableService
        self.tableName = tableName
        self.maxTelemetriesPerRow = maxTelemetriesPerRow

    def persistWidget(self, w:Widget, rowId:str):

        d = {
            "PartitionKey": w.factory_id +":" + w.line_id,
            "row_id": rowId,
            "serial_number": w.serial_number,
            "factory_id": w.factory_id,
            "line_id": w.line_id
        }
        for i,v in w.classification.to_dict()[1].items():
            d["classification_" + i] = v

        for sliceNumber in range(0, max(1, (len(w.telemetry) + self.maxTelemetriesPerRow - 1) // self.maxTelemetriesPerRow)):
            d["RowKey"] = str(int(w.classification.classified_time.replace(tzinfo=timezone.utc).timestamp())) +"-" + rowId + "-" + str(sliceNumber)
            d["telemetry"] = "[" + ", ".join([t.to_json() for t in w.telemetry[(sliceNumber * self.maxTelemetriesPerRow):((sliceNumber + 1) * self.maxTelemetriesPerRow)]]) + "]"
            print(d)

            # Insert the entity into the table
            print('Inserting a new entity into table - ' + self.tableName)
            print('Entity ' + str(d))
            self.tableService.insert_entity(self.tableName, d)
            print('Successfully inserted the new entity')