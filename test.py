import flet as ft
import cv2
import base64
import numpy as np
import threading


class VideoPlayer(ft.UserControl):
    def __init__(self, src=0):
        super().__init__()
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.thread = None

    def build(self):
        self.img_control = ft.Image()
        return self.img_control

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.update, daemon=True)
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.cap.release()
            self.thread.join()
            self.thread = None

    def update(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode()
            self.img_control.src = f"data:image/jpeg;base64,{jpg_as_text}"
            self.img_control.update()


def main(page: ft.Page):
    page.title = "Video Player"
    video_player = VideoPlayer(
        src="rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9")
    page.add(video_player)

    def start_button_clicked(e):
        video_player.start()

    def stop_button_clicked(e):
        video_player.stop()

    start_button = ft.ElevatedButton("Start", on_click=start_button_clicked)
    stop_button = ft.ElevatedButton("Stop", on_click=stop_button_clicked)

    page.add(start_button, stop_button)


ft.app(target=main)
