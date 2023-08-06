from ttcv.import_basic_utils import *
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
import numpy as np

class BaseDetectron():
    def get_model(self, cfg_file, score_thresh=0.5):
        cfg = get_cfg()
        cfg.merge_from_file(cfg_file)
        # cfg.DATASETS.TEST = self.args.test_dataset
        # cfg.DATALOADER.NUM_WORKERS = self.args.num_workers
        # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = self.args.batch_size_per_image
        # cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.args.num_classes  # only has one class (ballon)
        # cfg.MODEL.ANCHOR_GENERATOR.SIZES = self.args.anchor_sizes
        # cfg.MODEL.WEIGHTS = self.args.checkpoint
        # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.args.score_thresh_test

        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = score_thresh
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = score_thresh
        cfg.freeze()

        self.model = DefaultPredictor(cfg)

    def run(self, im, thresh=None, classes=None):
        return self.model(im)["instances"].to("cpu")
    
    def run_extract(self, predictions):
        boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
        scores = predictions.scores.numpy() if predictions.has("scores") else None
        classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None
        keypoints = predictions.pred_keypoints.numpy() if predictions.has("pred_keypoints") else None
        
        aa = 1
        


def test_base_detectron(cfg_file, score_thresh=0.5):
    detector = BaseDetectron()
    detector.get_model(cfg_file=cfg_file, score_thresh=score_thresh)
    
    







