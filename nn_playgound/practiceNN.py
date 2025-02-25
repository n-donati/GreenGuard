import tensorflow as tf
import numpy as np

print("TensorFlow version: ", tf.__version__)
# mnist is the well known hand written digit dataset
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
# las imágenes son de 0 a 255 por pixel, entonces los normalizamos de 0 a 1
x_train, x_test = x_train/255.0, x_test/255.0

# Para crear mi modelo

  # dropout applies to the outputs of the ReLU activation layer and before entering the next layer (softmax)
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

# converting the tensor to a numpy array after taking the first image as input, here you are TESTING AND PREDICTING BEFORE TRAINING. that is why it is only one image

predictions = model(x_train[0:1]).numpy()
print(predictions)

# si bien podrias incorporar este softmax como una activacion a la ultima capa del modelo, no se recomienda por que imposibilita el calculo preciso y estable para modelos que tienen como salida softmax.
tf.nn.softmax(predictions).numpy()

# aplicamos la función de perdida 
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# corroborando la pérdida inicial
print(loss_fn(y_train[:1], predictions).numpy())

# compilamos el modelo ANTES de entrenarlo
model.compile(optimizer='adam', 
              loss=loss_fn,
              metrics=['accuracy'])

# con model.fit ajustamos los parámetros para minimizar la función de pérdida
model.fit(x_train, y_train, epochs=5)

# evaluamos el modelo, verbose controls the level of detail of the output displayed 
model.evaluate(x_test, y_test, verbose=2)

# save my model to a file
# Save the entire model as a SavedModel.
model.export('saved_model/my_model')


