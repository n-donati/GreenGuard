import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.callbacks import ReduceLROnPlateau
import os
from PIL import Image

def resize_large_images(directory, target_size=(224, 224)):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    if img.size[0] > target_size[0] or img.size[1] > target_size[1]:
                        print(f"Resizing large image: {file}")
                        img = img.resize(target_size)
                        img.save(file_path)  # Overwrite the original file

# Function to filter allowed image formats (JPEG, PNG, GIF, BMP)
def filter_image_formats(directory):
    allowed_extensions = ['jpeg', 'png', 'gif', 'bmp']
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not any(file.lower().endswith(ext) for ext in allowed_extensions):
                print(f"Removing unsupported file format: {file}")
                os.remove(os.path.join(root, file))

train_dataset_path = 'tomato_dataset/train'
validation_dataset_path = 'tomato_dataset/valid'

# # Filter files in both training and validation directories
# filter_image_formats(train_dataset_path)
# filter_image_formats(validation_dataset_path)

# # Apply resizing to both training and validation directories
# resize_large_images(train_dataset_path)
# resize_large_images(validation_dataset_path)

print("Done filtering and rezising")

train_dataset = image_dataset_from_directory(
    train_dataset_path,
    image_size=(224, 224),
    batch_size=128
)

validation_dataset = image_dataset_from_directory(
    validation_dataset_path,
    image_size=(224, 224),
    batch_size=128
)

class_names = train_dataset.class_names

lr_scheduler = ReduceLROnPlateau(
    monitor='val_loss',  # Monitor the validation loss to adjust the learning rate
    factor=0.5,          # Reduce the learning rate by a factor of 0.5
    patience=3,          # Number of epochs with no improvement after which learning rate will be reduced
    min_lr=1e-6,         # Lower bound on the learning rate
    verbose=1            # Print updates about learning rate reduction
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(class_names), activation='softmax')
])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=8,
    callbacks=[lr_scheduler] 
)

model.evaluate(validation_dataset, verbose=2)

# model.save('rice_model.h5')  # Saves to HDF5 format
model.export('tomato_final')
