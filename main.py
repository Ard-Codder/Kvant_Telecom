from kivy.app import App
from kivy.core.image import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
import cv2
import requests
import numpy as np
from PIL import Image
from io import BytesIO


class CameraApp(App):
    def build(self):
        self.video = Video()
        layout = BoxLayout()
        layout.add_widget(self.video)
        return layout

    def start(self):
        url = 'https://watcher.tv.kvant-telecom.ru/4a9020a6-df34-4ee2-9dc6-55e1e6344a2e'
        self.get_video(url)

    def get_video(self, url):
        while True:
            response = requests.get(url)
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, -1)
            img = Image.fromarray(frame)
            buf = BytesIO()
            img.save(buf, format="jpeg")
            buf.seek(0)
            self.video.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            self.video.texture.blit_buffer(buf.read(), colorfmt='rgb', bufferfmt='ubyte')


if __name__ == '__main__':
    CameraApp().run()
