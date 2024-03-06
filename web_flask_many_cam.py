import cv2
from flask import Flask, render_template, Response, request

app = Flask(__name__)

# URL-адреса камер
camera_urls = [
    'rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9',
    'rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9',
    'rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9',
]


def get_video_feed(camera):
    # Для примера используем первую камеру из списка
    camera_url = camera

    # Создание объекта VideoCapture для указанной камеры
    cap = cv2.VideoCapture(camera_url)

    while True:
        # Чтение кадра с камеры
        ret, frame = cap.read()

        if not ret:
            break

        # Преобразование изображения в JPEG
        _, jpeg = cv2.imencode('.jpg', frame)

        # Отправка изображения через генератор
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    # Освобождение ресурсов
    cap.release()


@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/video_feed')
def video_feed():
    camera = request.args.get('camera')
    if camera is None:
        # Для примера используем первую камеру из списка
        camera = camera_urls[0]
    return Response(get_video_feed(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
