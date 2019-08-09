import os
import tarfile
import tempfile

from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.ml.score import score
from azure.storage.blob import BlockBlobService


class MLModelStorageDAO:

    def __init__(self, blobService: BlockBlobService, container: str):
        self.blobService = blobService
        self.container = container

    def classify_widget(self, w: Widget) -> Widget_Classification:
        with tempfile.TemporaryDirectory() as tmpdir:
            tar_archive = os.path.join(tmpdir, "model.tar.gz")
            self.blobService.get_blob_to_path(
                self.container, "anomaly.tar.gz", tar_archive)
            tar = tarfile.open(tar_archive, "r:gz")
            tar.extractall(tmpdir)
            classification: Widget_Classification = score(
                os.path.join(tmpdir, "model"), w)
            return classification
