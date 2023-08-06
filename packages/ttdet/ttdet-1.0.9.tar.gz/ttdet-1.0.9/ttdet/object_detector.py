import numpy as np
from time import time
import cv2
from ttcv.import_basic_utils import *

class ObjectDetector():
    def get_model(self, config_file, checkpoint_file):
        self.model = None

    def run(self, im, thresh=None, classes=None):
        return {'boxes': [], 'scores': [], 'classes': []}


    def predict_array(self, anArray, need_rot=False, test_shape=None, lefttop=(0,0), classes=None, thresh=None, sort=None):
        h,w = anArray.shape[:2]
        if need_rot: im_rot = cv2.rotate(anArray, cv2.ROTATE_90_CLOCKWISE)           # 90 rot
        else: im_rot = anArray

        need_reshape = (test_shape is not None)
        if need_reshape:
            h1, w1 = im_rot.shape[:2]
            im_scale = cv2.resize(im_rot, test_shape, interpolation=cv2.INTER_CUBIC)
            h2, w2 = im_scale.shape[:2]
            fx, fy = w1/w2, h1/h2       # restore ratios
        else: im_scale = im_rot

        ret = self.run(im_scale, thresh=thresh, classes=classes)
        boxes, scores, bclasses = ret['boxes'], ret['scores'], ret['classes']
        if len(classes)==0: return None

        if need_reshape: boxes[:, [0,2]], boxes[:, [1,3]] = boxes[:, [0,2]]*fx, boxes[:, [1,3]]*fy

        # ProcUtils().imshow(self.show_boxes(im_rot, boxes, bclasses))
        # cv2.waitKey()

        if need_rot:
            boxes = boxes[:,[1,2,3,0]]
            boxes[:,[1,3]] = h-boxes[:,[1,3]]

        # ProcUtils().imshow(self.show_boxes(anArray, boxes, bclasses))
        # cv2.waitKey()

        if lefttop !=(0,0): boxes[[0,2], :], boxes[[1,3], :] = boxes[[0,2], :] + lefttop[0], boxes[[1,3], :]+ lefttop[1]

        if sort is not None:
            if sort=='des': inds = np.argsort(np.array(scores.flatten()))[::-1]
            if sort == 'inc': inds = np.argsort(np.array(scores.flatten()))
            inds = inds.tolist()
            boxes = boxes[inds, :]
            scores = scores[inds, :]
            bclasses = [bclasses[j] for j in inds]


        return {'boxes': boxes, 'scores': scores.reshape((-1,1)), 'classes': bclasses}

    def show_boxes(self, im, boxes, labels=None, colors=None, line_thick=2, text_scale=1, text_thick=2):
        out = np.copy(im)
        for j, box in enumerate(boxes):
            if colors is None: color = (0,255,0)
            else: color = colors[j]

            left, top, right, bottom = box[:4]
            left, top, right, bottom = int(left), int(top), int(right), int(bottom)
            out = cv2.rectangle(out,(left,top),(right,bottom), color, line_thick)

            if labels is not None:
                out = cv2.putText(out, labels[j], (left, top), cv2.FONT_HERSHEY_COMPLEX,
                              text_scale, color, text_thick)
        return out









