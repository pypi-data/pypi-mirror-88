from ttcv.import_basic_utils import *
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
import numpy as np
from .object_detector import ObjectDetector
from .base_detectron import BaseDetectron

class FasterRCNNDetectron(BaseDetectron, ObjectDetector):

    def run(self, im, thresh=None, classes=None):
        ret = super().run(im=im, thresh=thresh, classes=classes)
        boxes = ret.pred_boxes.tensor.numpy()
        scores = ret.scores.numpy()
        bclasses = ret.pred_classes.numpy()
        bclasses = [classes[j] for j in bclasses] if classes is not None else bclasses.tolist()
        return {'boxes': boxes, 'classes':bclasses, 'scores': scores}


def test_fasterrcnn_detectron(cfg_file, score_thresh=0.5):
    detector = FasterRCNNDetectron()
    detector.get_model(cfg_file=cfg_file, score_thresh=score_thresh)







