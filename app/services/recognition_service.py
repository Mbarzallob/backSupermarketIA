from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import pandas as pd

threshold_optimo = 0.3
model = tf.keras.models.load_model("/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/services/modelo_cnn_multietiqueta.h5")  # si lo 
etiquetas = pd.read_csv('/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/assets/annotations_multietiqueta.csv').columns[1:] 
    
def recognize_product(ruta_imagen, threshold=threshold_optimo):
    try:
        img_ext = load_img(ruta_imagen, target_size=(128, 128))
        img_array = img_to_array(img_ext) / 255.0

        pred = model.predict(np.expand_dims(img_array, axis=0))[0]
        pred_bin = (pred > threshold).astype(int)
        etiquetas_detectadas = [etiquetas[i] for i, v in enumerate(pred_bin) if v == 1]

        top_indices = np.argsort(pred)[-3:][::-1]


        print(f"Clases detectadas (threshold {threshold}): {etiquetas_detectadas if etiquetas_detectadas else 'Ninguna'}")
        print("Top-3 más probables:")
        for i, idx in enumerate(top_indices):
            if(pred[idx] > threshold):
                return etiquetas[idx]
        
    except Exception as e:
        print(f"⚠️ Error al procesar la imagen: {e}")
