from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# URL видеопотока
url = 'rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9'


# Функция для получения кадров видеопотока
def get_frames():
    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()

        if ret:
            # Кодируем кадр в формат JPEG
            _, jpeg = cv2.imencode('.jpg', frame)

            # Преобразуем из массива байтов в строку
            jpeg = jpeg.tobytes()

            # Выдаем кадр в формате JPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')
        else:
            break

    cap.release()


# Обработчик главной страницы
@app.route('/')
def index():
    return render_template('index.html')


# Обработчик видеопотока
@app.route('/video')
def video():
    return Response(get_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
