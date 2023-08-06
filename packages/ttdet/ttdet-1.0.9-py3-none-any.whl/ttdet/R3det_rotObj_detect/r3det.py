# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os, sys
import tensorflow as tf
import time
import cv2
import argparse
import numpy as np
sys.path.append(os.path.join(os.getcwd(), 'KAI/detector/R3det_rotObj_detect'))

from dataio.image_preprocess import short_side_resize_for_inference_data
from configs.grasp_detection import r3det_configs as cfgs
from libs.networks import build_whole_network_r3det
from libs.box_utils import draw_box_in_img
from help_utils import tools

from KAI.basic.basic_objects import BasDetectObj
from KAI.policy.sequence_show_predict import SeqPredictor

class R3Detector(BasDetectObj):

    def get_model(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = '0'
        self.model = build_whole_network_r3det.DetectionNetwork(base_network_name=cfgs.NET_NAME,
                                                                 is_training=False)

        # 1. preprocess img
        self.img_plac = tf.placeholder(dtype=tf.uint8, shape=[None, None, 3])  # is RGB. not GBR
        self.img_batch = tf.cast(self.img_plac, tf.float32)
        self.img_batch = short_side_resize_for_inference_data(img_tensor=self.img_batch,
                                                         target_shortside_len=cfgs.IMG_SHORT_SIDE_LEN,
                                                         length_limitation=cfgs.IMG_MAX_LENGTH)
        if cfgs.NET_NAME in ['resnet152_v1d', 'resnet101_v1d', 'resnet50_v1d']:
            self.img_batch = (self.img_batch / 255 - tf.constant(cfgs.PIXEL_MEAN_)) / tf.constant(cfgs.PIXEL_STD)
        else:
            self.img_batch = self.img_batch - tf.constant(cfgs.PIXEL_MEAN)
        self.img_batch = tf.expand_dims(self.img_batch, axis=0)  # [1, None, None, 3]

        self.detection_boxes, self.detection_scores, self.detection_category = self.model.build_whole_detection_network(
            input_img_batch=self.img_batch,
            gtboxes_batch_h=None,
            gtboxes_batch_r=None)

        self.init_op = tf.group(
            tf.global_variables_initializer(),
            tf.local_variables_initializer()
        )

        self.restorer, self.restore_ckpt = self.model.get_restorer()

        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
    def detect(self, inputs):

        raw_img = inputs['rgb']

        with tf.Session(config=self.config) as sess:
            sess.run(self.init_op)
            if not self.restorer is None:
                self.restorer.restore(sess, self.restore_ckpt)
                print('restore model')

            start = time.time()
            resized_img, detected_boxes, detected_scores, detected_categories = \
                sess.run(
                    [self.img_batch, self.detection_boxes, self.detection_scores, self.detection_category],
                    feed_dict={self.img_plac: raw_img[:, :, ::-1]}  # cv is BGR. But need RGB
                )
            end = time.time()
            # print("{} cost time : {} ".format(img_name, (end - start)))

            show_indices = detected_scores >= cfgs.VIS_SCORE
            show_scores = detected_scores[show_indices]
            show_boxes = detected_boxes[show_indices]
            show_categories = detected_categories[show_indices]

            draw_img = np.squeeze(resized_img, 0)

            if cfgs.NET_NAME in ['resnet152_v1d', 'resnet101_v1d', 'resnet50_v1d']:
                draw_img = (draw_img * np.array(cfgs.PIXEL_STD) + np.array(cfgs.PIXEL_MEAN_)) * 255
            else:
                draw_img = draw_img + np.array(cfgs.PIXEL_MEAN)
            final_detections = draw_box_in_img.draw_boxes_with_label_and_scores(draw_img,
                                                                                boxes=show_boxes,
                                                                                labels=show_categories,
                                                                                scores=show_scores,
                                                                                method=1,
                                                                                in_graph=False)
            return  final_detections[:, :, ::-1]



class SeqR3DetectObj(SeqPredictor):
    def get_model(self):
        self.model = R3Detector(cfg_path=self.cfg_path)
        self.detector = self.model.detect

    def detect(self, rgbd, filename='unnamed'):

        return self.detector(inputs=rgbd.todict())


if __name__ == '__main__':
    cfg_path = 'configs/grasp_detection/r3det.cfg'
    SeqR3DetectObj(cfg_path=cfg_path).run()
















