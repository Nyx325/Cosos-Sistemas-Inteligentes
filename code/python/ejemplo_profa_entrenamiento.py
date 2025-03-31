import numpy as np
from keras.models import Sequential
from keras.layers import Dense

patrones=np.array([[0,0],[0,1],[1,0],[1,1]])

salida=np.array([[0], [1], [1], [0]])

model=Sequential()
model.add(Dense(16,input_dim=2, activation="relu"))
model.add(Dense(1,activation="sigmoid"))

model.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=["binary_accuracy"]
)

model.fit(patrones, salida, epochs=200)

scores=model.evaluate(patrones,salida)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
model.save("modelo_perceptron")
