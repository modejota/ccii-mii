import cv2, base64
import numpy as np
from urllib.request import urlopen


def handle(req):
    img_from_url = urlopen(req)
    img = cv2.imdecode(np.asarray(bytearray(img_from_url.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    _, imagen_jpeg = cv2.imencode('.jpeg', img)
    imagen_base64 = base64.b64encode(imagen_jpeg).decode('utf-8')
    return imagen_base64