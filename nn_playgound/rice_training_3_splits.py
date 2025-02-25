import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.preprocessing import image
import numpy as np

path = 'Rice_Leaf_AUG'

full_dataset = image_dataset_from_directory(
    path,
    seed=123,
    image_size=(256, 256),
    batch_size=32,
    shuffle=True
)

# get the classes
class_names = full_dataset.class_names
print(class_names)

# Step 2: Calculate the sizes for each split
dataset_size = tf.data.experimental.cardinality(full_dataset).numpy()
train_size = int(0.7 * dataset_size)
val_size = int(0.15 * dataset_size)
test_size = int(0.15 * dataset_size)

# Step 3: Create the splits
train_dataset = full_dataset.take(train_size)
remaining = full_dataset.skip(train_size)
validation_dataset = remaining.take(val_size)
test_dataset = remaining.skip(val_size)


model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2,2)),
    # tf.keras.layers.Conv2D(128, (3,3), activation='relu', padding='same'),
    # tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.Flatten(),
     tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(256, activation='relu'),
             tf.keras.layers.Dropout(0.5),
       tf.keras.layers.Dense(len(class_names), activation='softmax')
])


model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=7
)

model.evaluate(train_dataset, verbose=2)

# model.save('my_model.h5')  # Saves to HDF5 format
model.export('rice_model')
