import cv2, base64
import numpy as np

def save_image_from_base64(string, filename):
     # Decodificar el string base64 y almacenar los bytes en un objeto de tipo bytes
    decoded_data = base64.b64decode(string)
    np_data = np.frombuffer(decoded_data, np.uint8)

    # Decodificar los bytes en una imagen OpenCV
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    # Comprobar si el nombre de archivo especificado ya incluye la extensión ".jpg" o ".jpeg"
    if not filename.lower().endswith(('.jpg', '.jpeg')):
        filename += ".jpg"

    # Guardar la imagen con el nombre especificado
    return cv2.imwrite(filename, img)
