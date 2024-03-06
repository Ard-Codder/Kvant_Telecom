import cv2
import numpy as np
import sqlite3
import flet as ft
from flet import *
from yolov5 import YOLOv5


# Создание функции проверки авторизации
def check_auth(login, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE login=? AND password=?', (login, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True
    else:
        return False


# Создание функции регистрации нового пользователя
def register_user(login, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
    conn.commit()
    conn.close()


# Создание функции обработки нажатия кнопки "Login"
def login_click(e):
    login = login_input.value
    password = password_input.value
    if check_auth(login, password):
        # Авторизация прошла успешно, отображаем видеокамеры и прочий функционал
        page.clean()
        page.add(camera_view, label_text)
        update_image()
    else:
        # Авторизация не прошла, отображаем сообщение об ошибке
        login_form.value = 'Login error'
        login_form.update()


# Создание функции обработки нажатия кнопки "Register"
def register_click(e):
    # Отображаем форму регистрации нового пользователя
    page.clean()
    page.add(
        ft.Text('Register:', font_size=24),
        ft.TextField(hint_text='Enter login', on_change=lambda e: set_login_value(e)),
        ft.TextField(hint_text='Enter password', password=True, on_change=lambda e: set_password_value(e)),
        ft.ElevatedButton('Register', on_click=register_user_click)
    )
    page.update()


# Создание функции обновления изображения
def update_image():
    # Чтение кадра с камеры
    ret, frame = cap.read()

    # Изменение размера кадра для отображения в окне
    frame = cv2.resize(frame, (window_width, window_height))

    # Преобразование изображения в формат, подходящий для отображения в приложении
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode()
    img_src = f'data:image/jpeg;base64,{img_base64}'

    # Обновление изображения в элементе camera_view
    camera_view.src = img_src

    # Обработка изображения нейронной сетью YOLO
    boxes = yolo.detect_image(frame)

    # Отображение результатов обработки на изображении
    for box in boxes:
        x, y, w, h = box[:4]
        label = box[4]
        score = box[5]
        color = (255, 0, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f'{label} {score:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Обновление текстового поля с результатами обработки
    label_text.value = f'Objects detected: {len(boxes)}'

    # Запуск функции обновления изображения через 30 миллисекунд
    ft.Timer(30, update_image).start()


# Создание функции обработки нажатия кнопки "Register" в форме регистрации
def register_user_click(e):
    login = login_input.value
    password = password_input.value
    register_user(login, password)
    # Возврат на страницу авторизации
    page.clean()
    page.add(login_form, login_input, password_form, password_input, login_button, register_button)
    page.update()


# Создание приложения
def main(page: Page):
    # Создание таблицы пользователей в базе данных при первом запуске приложения
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (login TEXT, password TEXT)''')
    conn.commit()
    conn.close()

    # Отображение формы авторизации
    page.add(login_form, login_input, password_form, password_input, login_button, register_button)


# Загрузка нейронной сети YOLO
yolo = YOLOv5()

# Создание объекта камеры
cap = cv2.VideoCapture('https://watcher.tv.kvant-telecom.ru/vsaas/v2/cameras/pyaterochka.test-132ba24f9a/view')

# Определение размера окна просмотра видео
window_width = 640
window_height = 480

# Создание элементов интерфейса
camera_view = ft.Image(src=None, width=window_width, height=window_height)
label_text = ft.Text('')
login_form = ft.Text('Login:', font_size=24)
password_form = ft.Text('Password:', font_size=24)
login_input = ft.TextField(hint_text='Enter login')
password_input = ft.TextField(hint_text='Enter password', password=True)
login_button = ft.ElevatedButton('Login', on_click=login_click)
register_button = ft.TextButton('Register', on_click=register_click)

# Запуск приложения
ft.app(target=main)
