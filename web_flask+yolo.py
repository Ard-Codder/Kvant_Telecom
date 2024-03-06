import torch
import cv2
import numpy as np
from flask import Flask, render_template, Response

# Загрузка модели YOLO
model = torch.hub.load('WongKinYiu/yolov7', 'custom', path='8s/weights/best.pt', source='local')
model.eval()

# Загрузка видеопотока
cap = cv2.VideoCapture("rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9")

# Определение размера кадра
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Определение генератора для получения кадров видеопотока
def get_frames():
    while True:
        # Чтение кадра
        ret, frame = cap.read()

        if not ret:
            break

        # Преобразование кадра в формат, подходящий для обработки YOLO
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 640))
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        img = torch.from_numpy(img)
        img = img.float()
        img /= 255.0

        # Обработка кадра с помощью YOLO
        with torch.no_grad():
            predictions = model(img)
            predictions = predictions[0]

        # Отображение обнаруженных объектов на кадре
        for i in range(predictions.shape[0]):
            box = predictions[i, :4]
            x1, y1, x2, y2 = map(int, box)
            x1, y1, x2, y2 = map(lambda x: max(0, min(x, frame_width, frame_height)), (x1, y1, x2, y2))
            class_id = int(predictions[i, 5])
            confidence = float(predictions[i, 4])
            label = f"{model.names[class_id]} {confidence:.2f}"
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Кодирование кадра в формат JPEG
        _, jpeg = cv2.imencode('.jpg', frame)

        # Преобразование из массива байтов в строку
        jpeg = jpeg.tobytes()

        # Выдача кадра в формате JPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')

    cap.release()

# Создание приложения Flask
app = Flask(__name__)

# Определение маршрута для отображения видеопотока
@app.route('/video')
def video():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Определение маршрута для отображения главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
