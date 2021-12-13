import os
import numpy as np
import autokeras as ak
from tensorflow.keras.models import load_model

from ..predict import BasePredictor
from ..utils import Normalizer
from .. import TUNER_PROJECT_NAME
from .. import TUNER_MODEL_FOLDER


class Predictor(BasePredictor):
    def __init__(self, model_dir):
        BasePredictor.__init__(self, model_dir=model_dir)

    def predict(self, idxs=None, head=None, tail=None):
        X = self._get_X(idxs=idxs, head=head, tail=tail)
        mdl_path=os.path.join(self.model_dir, TUNER_PROJECT_NAME, TUNER_MODEL_FOLDER)
        if not os.path.exists(mdl_path):
            print("not Found")
        mdl = load_model(mdl_path, custom_objects=ak.CUSTOM_OBJECTS)
        output_data = mdl.predict(X)
        print(output_data)
        y = np.array(output_data)
        n = Normalizer()
        n.load(self.model_dir)
        return n.inverse_transform(y)