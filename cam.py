import cv2

# URL видеопотока
url = 'rtsp://w3.tv.kvant-telecom.ru/chursina.6.lovim.vora-a41ab39a2a?dvr=true&token=2.9omxv2sXAx0ABfmU4bRWyqbRoCvKJ50hlMIAlSbQjP-EIid9'

# Создаем объект захвата видео
cap = cv2.VideoCapture(url)

while True:
    # Читаем кадр
    ret, frame = cap.read()

    # Если кадр прочитан успешно
    if ret:
        # Отображаем кадр
        cv2.imshow('Video', frame)

        # Выходим из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
