import cv2
import numpy as np
from matplotlib import pyplot as plt
from glob import  glob
import os

def matching(img_gray, template, threshold=0.5):
    height, width = template.shape[:2]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    Y,X = np.where( res >= threshold)
    boxes, scores = [], []
    for y,x in zip(Y,X):
        boxes.append([int(x), int(y), int(x+width), int(y+height)])
        scores.append(float(res[(y,x)]))
    # print('{} {} boxes matched'.format('+'*10, len(boxes)))
    return boxes, scores

def matching_multi(img_gray, templates,threshold=0.5, test_scales=[1,]):
    boxes, scores = [], []
    for s in test_scales:
        test_im = np.copy(img_gray)
        if s!=1: test_im = cv2.resize(test_im, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
        boxes_, scores_ = [], []
        for tmp_im in templates:
            bb, ss= matching(img_gray=test_im, template=tmp_im, threshold=threshold)
            boxes_ += bb
            scores_ += ss
        if s!=1: boxes_, scores_ = (np.array(boxes_)/(s+0.0000001)).tolist(), (np.array(scores_)/(s+0.0000001)).tolist()
        boxes, scores = boxes + boxes_, scores + scores_

    return boxes, scores

def matching_dir(img_gray, template_dir,threshold=0.5):
    tmp_ims = [cv2.imread(path, cv2.IMREAD_GRAYSCALE)
               for path in glob(os.path.join(template_dir, '*'))]
    boxes, scores = matching_multi(img_gray, tmp_ims, threshold=threshold)
    # print('{} {} boxes matched'.format('+'*10, len(boxes)))
    return boxes, scores


if __name__=='__main__':
    img_rgb = cv2.imread('test_images/SourceIMG.jpeg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('test_images/TemplateIMG.jpeg', 0)

    boxes = match(img_gray, template)
    for box in boxes:
        cv2.rectangle(img_rgb, (box[0], box[1]), (box[2], box[3]), (0,255,0), 2)

    cv2.imshow('im', img_rgb)
    cv2.waitKey()
