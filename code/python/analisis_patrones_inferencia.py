import cv2
import numpy as np
import tensorflow as tf

modelo = tf.keras.models.load_model("modelo_perceptronFigG.keras")

imagen = cv2.imread("imagen.png")
imagen = cv2.resize(imagen, (64, 64))
cv2.imshow("Imagen", imagen)
imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
borde = cv2.Canny(imagen, 100, 200)
imagen = borde.astype("float32") / 255.0  # Normalizar entre 0 y 1


x_test = tf.convert_to_tensor(
    np.array(imagen).reshape((1, 64, 64, 1)), dtype=tf.float32
)

prediccion = modelo.predict(x_test)
prediccion_int = np.argmax(prediccion)
print("Predicción ", prediccion, "      ", prediccion_int)
cv2.waitKey(0)
cv2.destroyAllWindows()
