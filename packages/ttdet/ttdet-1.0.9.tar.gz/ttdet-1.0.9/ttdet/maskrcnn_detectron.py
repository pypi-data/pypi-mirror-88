from ttcv.import_basic_utils import *
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
import numpy as np

class MaskRCNNDetectron():
    def get_model(self):
        self.model = DefaultPredictor(self.cfg)

    def load_params(self,args):
        self.args=args
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file(self.args.config_file))
        # cfg.DATASETS.TEST = self.args.test_dataset
        # cfg.DATALOADER.NUM_WORKERS = self.args.num_workers
        # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = self.args.batch_size_per_image
        # cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.args.num_classes  # only has one class (ballon)
        # cfg.MODEL.ANCHOR_GENERATOR.SIZES = self.args.anchor_sizes
        # cfg.MODEL.WEIGHTS = self.args.checkpoint
        # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.args.score_thresh_test

        self.cfg.MODEL.RETINANET.SCORE_THRESH_TEST = self.args.score_thresh
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.args.score_thresh
        self.cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = self.args.score_thresh
        self.cfg.freeze()

    def predict_array(self, im):
        ret = self.detector(im)["instances"].to("cpu")
        boxes = ret.pred_boxes.tensor.numpy()
        masks = ret.pred_masks.numpy().astype('uint8')
        classes = ret.pred_classes.numpy()
        scores = ret.scores.numpy()

        return {'boxes': boxes, 'masks': masks, 'classes':classes, 'scores': scores}

    def show_detect_results(self, im, detect_rets):
        boxes = detect_rets['boxes']
        masks = detect_rets['masks']
        classes = detect_rets['classes']
        scores = detect_rets['scores']
        out = np.copy(im)
        obj_ind = 0
        num_detected = boxes.shape[0]
        if num_detected==0: return im

        for i in range(num_detected):
            cls = classes[i]
            score = scores[i]
            if cls == '__background__': continue
            box = boxes[i,:].astype('int')
            mask = masks[i, :,:]

            color = ProcUtils().get_color(obj_ind)

            left, top, right, bottom = box

            loc = np.where(mask)

            out[loc] = 0.8 * out[loc] + tuple(0.2 * np.array(color))
            cv2.rectangle(out, (left, top), (right, bottom), color, 2)
            cv2.putText(out, '%s: %d' %(cls, int(100*score)), (left, top-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)

            obj_ind += 1

        return out


def test_maskrcnn_detectron(cfg_path):
    detector = MaskRCNNDetectron()
    args = CFG(cfg_path=cfg_path)
    detector.load_params(args=args)
    detector.get_model()







