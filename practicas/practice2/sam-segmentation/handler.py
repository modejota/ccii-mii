import os, io, cv2, base64
import numpy as np
import matplotlib.pyplot as plt
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from urllib.request import urlopen


def handle(req):
    img_from_url = urlopen(req)
    img = cv2.imdecode(np.asarray(bytearray(img_from_url.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    sam = sam_model_registry['vit_l'](checkpoint=os.environ.get('MODEL_FILE'))
    sam.to(device='cpu') # Minikube en Windows no soporta GPU

    # start_time = time.time()
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img)
    # end_time = time.time()
    # print("Tiempo de ejecución:", end_time - start_time, "segundos")

    plt.figure(figsize=(20,20))
    plt.imshow(img)
    if len(masks) != 0:
        sorted_anns = sorted(masks, key=(lambda x: x['area']), reverse=True)
        ax = plt.gca()
        ax.set_autoscale_on(False)

        img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
        img[:,:,3] = 0
        for ann in sorted_anns:
            m = ann['segmentation']
            color_mask = np.concatenate([np.random.random(3), [0.35]])
            img[m] = color_mask
        ax.imshow(img)
        plt.axis('off')
        buffer = io.BytesIO()
        plt.savefig(buffer, bbox_inches='tight', pad_inches=0)
        imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    else:
        _, imagen_jpeg = cv2.imencode('.jpeg', img)
        imagen_base64 = base64.b64encode(imagen_jpeg).decode('utf-8')
    return imagen_base64