import cv2
import numpy as np

def nms_ids(boxes, scores, score_thresh=0.5, nms_thresh=0.7):
    # boxes = [[left, top, right, bottom]]
    boxes_array = np.array(boxes)               # convert to x,y,w,h
    boxes_array[:, 2] -= boxes_array[:,0]
    boxes_array[:, 3] -= boxes_array[:, 1]
    bboxes = boxes_array.tolist()

    idxs = cv2.dnn.NMSBoxes(bboxes, scores,
                            score_threshold=score_thresh, nms_threshold=nms_thresh).flatten()
    return idxs


def nms(boxes, scores, score_thresh=0.5, nms_thresh=0.7):
    idxs = nms_ids(boxes, scores, score_thresh, nms_thresh)
    return [boxes[i] for i in idxs], [scores[i] for i in idxs]


def nms_cross_category(boxes, scores, classes=None, select_classes=None, score_thresh=0.5, nms_thresh=0.7):
    if classes is None or select_classes is None:
        idxs = nms_inds(boxes, scores, score_thresh, nms_thresh)
        return {'boxes': boxes[idxs, :], 'scores': scores[idxs, :], 'classes': [classes[i] for i in idxs]}
    select_inds = [j for j,cls in enumerate(classes) if cls in select_classes]
    if len(select_inds)==0: return {'boxes': boxes, 'scores': scores, 'classes': classes}

    not_select_inds = [j for j,cls in enumerate(classes) if cls not in select_classes]

    idxs = nms_ids(boxes[select_inds, :], scores[select_inds, :].flatten().tolist(), score_thresh, nms_thresh)
    out_inds = not_select_inds +  [select_inds[i] for i in idxs]
    return {'boxes': boxes[out_inds, :], 'scores': scores[out_inds, :], 'classes': [classes[i] for i in out_inds]}

