from fastapi import FastAPI
import cv2
import requests
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

camera_url = 'https://watcher.tv.kvant-telecom.ru/vsaas/v2/cameras/pyaterochka.test-132ba24f9a/view'


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/video")
async def read_video():
    while True:
        response = requests.get(camera_url)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, -1)
        img = Image.fromarray(frame)
        buf = BytesIO()
        img.save(buf, format="jpeg")
        buf.seek(0)
        yield buf.read()
