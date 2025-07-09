import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import pandas as pd

def recognize_product(product_path:str):
    model = tf.keras.models.load_model("/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/services/supermarket_model.h5")  # si lo guardaste
    img_path = "/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/images/imagen.jpeg"
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]  
    preds_redondeadas = (preds > 0.5).astype(int)


    # --- Mostrar resultados
    etiquetas = pd.read_csv('/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/assets/annotations.csv').columns[1:]  # quitamos la columna 'file'
    resultado = dict(zip(etiquetas, preds_redondeadas))

    print("Etiquetas detectadas:")
    for k, v in resultado.items():
        print(f"{k}: {'Sí' if v == 1 else 'No'}")
        if v == 1:
            print(k)
            return k
