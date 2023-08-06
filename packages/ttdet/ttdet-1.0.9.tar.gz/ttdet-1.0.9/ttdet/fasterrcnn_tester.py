from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
from time import time
import configparser
import cv2
from ttcv.import_basic_utils import *
from ttcv.basic.basic_objects import BasDetectObj
from .object_detector import ObjectDetector

class FasterRCNNDetector(ObjectDetector):
    def get_model(self, config_file, checkpoint_file):
        self.model = init_detector(config_file, checkpoint_file, device='cuda:0')

    def run(self, im, thresh=None, classes=None):
        boxes_list = inference_detector(self.model, im)
        boxes, scores, bclasses = [], [], []
        for j, _boxes in enumerate(boxes_list):
            num_box = len(_boxes)
            if num_box == 0: continue
            if thresh is not None:
                _scores = _boxes[:, -1]
                _boxes = _boxes[_scores >= thresh, :]

            num_box = len(_boxes)
            if num_box == 0: continue
            boxes.append(_boxes[:, :4])
            scores.append(_boxes[:, -1].reshape((-1, 1)))
            if classes is None:
                bclasses += [j] * num_box
            else:
                bclasses += [classes[j]] * num_box

        if len(boxes) == 0: return None
        boxes = np.vstack(boxes)
        scores = np.vstack(scores)
        return {'boxes': boxes, 'scores': scores, 'classes': bclasses}









