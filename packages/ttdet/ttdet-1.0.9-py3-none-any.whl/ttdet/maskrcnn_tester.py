from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
from time import time
import configparser
import cv2

class MaskRCNNDetector():

    def get_model(self, config_file, checkpoint_file):
        self.model = init_detector(config_file, checkpoint_file, device='cuda:0')

    def predict_array(self, im, thresh=None, classes=None):
        boxes_list, masks_list = inference_detector(self.model, im)

        boxes, masks, scores, bclasses = [], [], [], []
        for j, _boxes in enumerate(boxes_list):
            num_box = len(_boxes)
            if num_box == 0: continue
            _masks = masks_list[j]
            if thresh is not None:
                _scores = _boxes[:, -1]
                _boxes = _boxes[_scores >= thresh, :]
                _masks = _masks[_scores >= thresh, :]

            num_box = len(_boxes)
            if num_box == 0: continue
            boxes.append(_boxes[:, :4])
            scores.append(_boxes[:, -1].reshape((-1, 1)))
            if classes is None: bclasses += [j]*num_box
            else: bclasses += [classes[j]]*num_box
            masks += [maskUtils.decode(msk).astype(np.uint8) for msk in _masks]

        boxes = np.vstack(boxes)
        scores = np.vstack(scores)

        return boxes, masks, scores, bclasses









