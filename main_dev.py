# -*- coding: utf-8 -*-
from detection import Detector
import time
import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock


Builder.load_file("main.kv")

Window.size = (1000, 600)


class ShowData(BoxLayout):

    def __init__(self, **kwargs):
        super(ShowData, self).__init__(**kwargs)

    def set_text(self, t):
        self.ids.send_body_json.text = t


class Editor(BoxLayout):
    def __init__(self, **kwargs):

        super(Editor, self).__init__(**kwargs)
        self.cam_show = True
        self.detector = Detector()
        self.img1 = Image(size_hint=(1.0, 0.8))
        self.showData = ShowData()

    def start_cam(self, src=0):
        self._cap = cv2.VideoCapture(src)
        while not self._cap.isOpened():
            pass
        self.cam_show = True
        print('cam started!')
        self.count = 0
        self.fps = 0
        self.start_time = time.time()

    def close_cam(self):
        self.cam_show = False
        self._cap.release()

    def update(self, dt):
        if self._cap.isOpened() is False:
            return

        _, img = self._cap.read()
        # get pose
        pose_img, send_pose = self.detector.detect(img)
        self.showData.set_text(send_pose)
        show_img = cv2.flip(pose_img, 0)
        # set texture
        texture1 = Texture.create(
            size=(show_img.shape[1], show_img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(show_img.tostring(),
                             colorfmt='bgr', bufferfmt='ubyte')
        # show the results
        if self.cam_show:
            self.img1.texture = texture1
        else:
            self.img1.texture = None

        self.count += 1
        if self.count == 10:
            self.calc_fps()

    def calc_fps(self):
        self.fps = 10 / (time.time() - self.start_time)
        self.count = 0
        self.start_time = time.time()

    # event handle
    def connect_zmq(self, ip_id, port_id):
        self.detector.disconnect_zmq()
        ip = ip_id.text
        port = int(port_id.text)
        print('connect zmq')
        self.detector.connect_zmq(ip, port)

    def cam_load(self, src):
        print('cam load', src.text)
        self.close_cam()
        if src.text.find('mp4') != -1 or src.text.find('m4a') != -1:
            self.start_cam(src.text)
        else:
            self.start_cam(int(src.text))

    def toggle_cam_show(self, cb):
        print(cb.active)
        self.cam_show = cb.active

    def change_scale(self, k):
        rk = round(k.value, 2)
        self.detector.set_scale_factor(rk)
        print('scale changed to', rk)

    def change_pose_num(self, k):
        ik = int(k.value)
        self.detector.set_pose_num(ik)
        print('pose num changed to', ik)

    def change_min_pose_score(self, k):
        rk = round(k.value, 2)
        print('min pose score changed to', rk)

    def change_min_part_score(self, k):
        rk = round(k.value, 2)
        print('min part score changed to', rk)


class CvCamera(App):
    def build(self):
        # UI
        layout = BoxLayout(orientation='vertical', size_hint=(1.0, 1.0))
        self.editor = Editor()
        layout.add_widget(self.editor)
        layout2 = BoxLayout(orientation='horizontal', size_hint=(1.0, 1.0))
        layout2.add_widget(self.editor.img1)
        layout2.add_widget(self.editor.showData)
        layout.add_widget(layout2)

        self.editor.start_cam()
        self.editor.detector.connect_zmq()
        self.editor.detector.load()

        Clock.schedule_interval(self.editor.update, 1.0/30.0)

        return layout

    def on_stop(self):
        self.editor.close_cam()


if __name__ == '__main__':
    CvCamera().run()
