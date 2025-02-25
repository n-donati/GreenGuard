import nncf
import tensorflow as tf
import os
import glob

# Step 1: Load the Calibration Dataset from Local Directory
calibration_data_dir = 'calibration_rice'

# Create a list of image file paths
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
image_paths = []
for ext in image_extensions:
    image_paths.extend(glob.glob(os.path.join(calibration_data_dir, '**', ext), recursive=True))

def load_and_preprocess_image(path):
    try:
        # Read the image file
        image = tf.io.read_file(path)
        # Decode the image
        image = tf.image.decode_image(image, channels=3)
        # Check if the image was successfully decoded
        if image.shape.rank != 3:
            print(f"Error: Unable to decode image {path}")
            return None
        # Resize the image to match your model's expected input size
        image = tf.image.resize(image, [256, 256])  # Adjust size as per your model
        # Normalize the image if required
        image = tf.image.convert_image_dtype(image, tf.float32)
        return image
    except Exception as e:
        print(f"Error processing image {path}: {str(e)}")
        return None

# Create the dataset
def filter_valid_images(image):
    return image is not None

calibration_loader = tf.data.Dataset.from_tensor_slices(image_paths)
calibration_loader = calibration_loader.map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
calibration_loader = calibration_loader.filter(filter_valid_images)

# Step 2: Define the Transform Function for NNCF
def transform_fn(data_item):
    # Add batch dimension if required
    data_item = tf.expand_dims(data_item, axis=0)
    return data_item

# Step 3: Create the NNCF Dataset
calibration_dataset = nncf.Dataset(calibration_loader, transform_fn)


# Quantize the model
quantized_model = nncf.quantize(model, calibration_dataset)

# Save the quantized model
tf.saved_model.save(quantized_model, "quantized_rice_model")
print("Quantization complete. Model saved as 'quantized_rice_model'")