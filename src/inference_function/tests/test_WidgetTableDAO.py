"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import copy
import json
from datetime import datetime, timezone
from unittest.mock import patch

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from azure.storage.table import TableService

from ProcessTelemetry.WidgetTableDAO import WidgetTableDAO


class TestWidgetTableDAO(object):
    """
    Test Suite against event WidgetTableDAO
    """

    @patch('azure.storage.table.TableService')
    def test_persist(self, mockTableService: TableService):
        """
        Tests to ensure the generator posts events to event hub
        """

        persisted_entities = []
        def captureCalls(table_name, entity):
            assert table_name == "Predictions"
            persisted_entities.append(copy.deepcopy(entity))
        mockTableService.insert_entity.side_effect = captureCalls

        dao = WidgetTableDAO(mockTableService, tableName="Predictions", maxTelemetriesPerRow=2)
        w = generate_widget()
        dao.persistWidget(w, "myid")

        assert len(persisted_entities) == 3
        assert persisted_entities[0]['PartitionKey'] == 'kitty hawk:1'
        assert persisted_entities[0]['RowKey'] == 'kitty hawk-devserial1'
        assert persisted_entities[1]['RowKey'] == 'kitty hawk-devserial1'
        assert persisted_entities[2]['RowKey'] == 'kitty hawk-devserial1'
        assert persisted_entities[0]['row_id'] == 'myid'
        assert persisted_entities[0]['serial_number'] == 'devserial1'
        assert persisted_entities[0]['factory_id'] == 'kitty hawk'
        assert persisted_entities[0]['line_id'] == '1'
        assert persisted_entities[0]['classification_std_dist'] == 1.0

        tels = [json.loads(p['telemetry']) for p in persisted_entities]
        assert len(tels[0]) == 2
        assert len(tels[1]) == 2
        assert len(tels[2]) == 1
        assert tels[0][0]['time_stamp'] == "2001-09-09T01:46:40+00:00"
        assert tels[1][1]['time_stamp'] == "2001-09-09T01:46:43+00:00"


def generate_classification() -> Widget_Classification:
    classification = Widget_Classification()
    classification.classified_time = datetime.fromtimestamp(1000000000, timezone.utc)
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    return classification

def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.classification = generate_classification()
    w.telemetry = [generate_telemetry() for i in range(0, 5)]
    return w

timestamp = 1000000000
def generate_telemetry() -> Telemetry:
    t = Telemetry()
    t.ambient_humidity = 10.
    t.ambient_temp = 20.
    t.amperage = 30.
    t.voltage = 40.2
    t.flux_capacitance = 50.
    global timestamp
    t.time_stamp = datetime.fromtimestamp(timestamp, timezone.utc)
    timestamp += 1
    return t
