"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.ml.base_alg import Base_Alg
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
import random
from datetime import datetime

class WidgetClassifier(Base_Alg):
    """
    ML Class that performs actual predictions.
    """
    x_scaler = None
    y_scaler = None
    model = None

    def load_model(self):
        return True

    def predict(self, data : Widget) -> Widget_Classification:
        wc = Widget_Classification()
        if(random.randint(0,100) > 90):
            wc.std_dist = 4
            wc.std = 5
        else:
            wc.std_dist = 0.5
            wc.std = 1.5
        wc.classified_time = datetime.utcnow()
        wc.threshold = 3
        wc.mean = 1
        return wc
