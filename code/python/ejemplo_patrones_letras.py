import numpy as np
from keras.models import Sequential
from keras.layers import Dense

patrones=np.array([
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
    ],
    [
        0,1,0,
        0,1,0,
        0,1,0,
        0,1,0,
        0,1,0
    ]
])

salida=np.array([0,1,2])

model=Sequential()
model.add(
    Dense(
        16, 
        input_dim=15, 
        activation="relu"
    )
)
model.add(
    Dense(
        8,
        activation="relu"
    )
)
model.add(
    Dense(
        3,
        activation="softmax"
    )
)



model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam",
    metrics=["sparse_categorical_accuracy"]
)

model.fit(patrones, salida, epochs=200)

scores=model.evaluate(patrones,salida)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
model.save("modelo_patrones")


