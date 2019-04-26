import tensorflow as tf
import time
import cv2
import posenet
import numpy as np
import gc

import json
from data_send import ZMQ_SENDER

IP = "127.0.0.1"
PORT = 5775

CAM_SRC = 0

POSE_MODEL = 101

SCALE_FACTOR = 0.1
MAX_POSE_DETECTIONS = 5
MIN_POSE_SCORE = 0.25
MIN_PART_SCORE = 0.1

B_SHOW = True


class Detector():
    def __init__(self):
        self.scale_factor = SCALE_FACTOR
        self.max_pose_detections = MAX_POSE_DETECTIONS
        self.min_pose_score = MIN_POSE_SCORE
        self.min_part_score = MIN_PART_SCORE
        self.port = PORT
        self.ip = IP
        self.data_send = ZMQ_SENDER()

    def connect_zmq(self, ip=IP, port=PORT):
        self.port = port
        self.ip = ip
        self.data_send.initialize(self.ip, self.port)

    def disconnect_zmq(self):
        self.data_send.close()

    def set_scale_factor(self, scale):
        self.scale_factor = scale

    def set_pose_num(self, num):
        self.max_pose_detections = num

    def set_min_pose_score(self, score):
        self.min_pose_score = score

    def set_min_part_score(self, score):
        self.min_part_score = score

    def make_dict(self, coords, scores):
        send_data = {}
        send_data["version"] = 0.1
        bodies = []

        # for each pose
        for pos, score in zip(coords, scores):
            if pos[0][0] == 0.0 and pos[0][1] == 0.0:
                continue

            value = {}
            values = []

            for _i in range(17):
                values.append(pos[_i][0])
                values.append(pos[_i][1])
                values.append(score[_i])

            value["joints"] = values
            bodies.append(value)

        send_data["bodies"] = bodies
        return send_data

    def load(self):

        self.sess = tf.InteractiveSession()

        self.model_cfg, self.model_outputs = posenet.load_model(
            POSE_MODEL, self.sess)
        self.output_stride = self.model_cfg['output_stride']

    def detect(self, img):

        input_image, display_image, output_scale = posenet.read_img(
            img, scale_factor=self.scale_factor, output_stride=self.output_stride)

        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = self.sess.run(
            self.model_outputs,
            feed_dict={'image:0': input_image}
        )

        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=self.output_stride,
            max_pose_detections=self.max_pose_detections,
            min_pose_score=self.min_pose_score)

        keypoint_coords *= output_scale
        overlay_image = posenet.draw_skel_and_kp(
            display_image, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_score=self.min_pose_score, min_part_score=self.min_part_score)

        send_pose = self.send_pose(keypoint_scores, keypoint_coords)

        return overlay_image, send_pose

    def send_pose(self, k_scores, k_coords):
        # send pose data
        send_dict = self.make_dict(k_coords, k_scores)
        self.data_send.send(send_dict)
        sd = json.dumps(send_dict)
        return sd
