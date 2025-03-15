import numpy as np
from keras.models import Sequential
import tensorflow as tf


modelo=tf.keras.models.load_model("modelo_patrones")
test = np.array([
    [
        1,0,1,
        1,0,1,
        1,0,1,
        1,0,1,
        1,1,1
    ],
    [
        1,1,0,
        1,0,0,
        1,1,0,
        1,0,0,
        1,1,0
    ]
])
prediccion = modelo.predict(test)
print(prediccion.round())