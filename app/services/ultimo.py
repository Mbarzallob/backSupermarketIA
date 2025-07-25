import os
import cv2
import tensorflow as tf
import pandas as pd
import numpy as np

IMAGE_SIZE = (224, 224)

# Cargar el modelo previamente entrenado
model = tf.keras.models.load_model("/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/models/modelo_cnn_transfer_learning_balanceado.h5")
class_names = pd.read_csv('/home/mateo/Documentos/Universidad/Sexto/InteligenciaArtificial/backend_productos/app/assets/annotations_val_multietiqueta.csv').columns[1:] 

def clasificar_imagen_externa(ruta_imagen, threshold=0.4):
    try:
        if not os.path.exists(ruta_imagen):
            return {"error": f"Archivo no encontrado: {ruta_imagen}"}
        
        
        img = cv2.imread(ruta_imagen)
        if img is None:
            return {"error": "No se pudo cargar la imagen. Verificar formato."}
        
        img = cv2.resize(img, IMAGE_SIZE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_processed = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        
        pred = model.predict(np.expand_dims(img_processed, axis=0), verbose=0)[0]
        pred_bin = (pred > threshold).astype(int)
        
        clases_detectadas = []
        for i, prob in enumerate(pred):
            if prob >= threshold:
                clases_detectadas.append({
                    'clase': class_names[i],
                    'probabilidad': float(prob),
                    'confianza': f"{prob*100:.1f}%"
                })
        
        clases_detectadas.sort(key=lambda x: x['probabilidad'], reverse=True)
        
        # Top 3 predicciones
        top_3 = []
        top_indices = np.argsort(pred)[-3:][::-1]
        for idx in top_indices:
            top_3.append({
                'clase': class_names[idx],
                'probabilidad': float(pred[idx]),
                'confianza': f"{pred[idx]*100:.1f}%"
            })
        
     
        
        if clases_detectadas:
            print(f"\\n CLASES DETECTADAS:")
            for i, det in enumerate(clases_detectadas[:5], 1):  # Máximo 5
                print(f"  {i}. {det['clase']}: {det['confianza']}")
        else:
            print(f"\\n No se detectaron clases con confianza >= {threshold}")
        
        print(f"\\n📊 TOP-3 MÁS PROBABLES:")
        for i, det in enumerate(top_3, 1):
            print(f"  {i}. {det['clase']}: {det['confianza']}")
        
        clases = [det['clase'] for det in clases_detectadas ]
        
        return clases
        
    except Exception as e:
        return {"error": f"Error procesando imagen: {str(e)}"}