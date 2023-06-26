import os, cv2, base64
import numpy as np
from urllib.request import urlopen

def handle(req):
    img_from_url = urlopen(req)
    img = cv2.imdecode(np.asarray(bytearray(img_from_url.read()), dtype=np.uint8), cv2.IMREAD_COLOR)

    # Cargar el modelo de red neuronal pre-entrenada. Tomamos las rutas de las variables de entorno de OpenFaaS.
    net = cv2.dnn.readNetFromCaffe(os.environ.get('PROTOTXT_FILE'), os.environ.get('CAFFE_MODEL_FILE'))
    h, w = img.shape[:2]
    # Red pre-entrenada para 300x300, pero con tamaños algo mayores da mejor resultado.
    # La última tripleta representa la media sustraída de cada canal de color de la imagen de entrada. Estos valores son específicos de la red neuronal pre-entrenada.
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (600, 600)), 1.0, (600, 600), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= 0.85:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)

    _, imagen_jpeg = cv2.imencode('.jpeg', img)
    imagen_base64 = base64.b64encode(imagen_jpeg).decode('utf-8')
    return imagen_base64
