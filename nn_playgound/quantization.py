import tensorflow as tf
import nncf
import os
import numpy as np
import openvino as ov


def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image

def load_dataset(data_dir):
    image_paths = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
    
    dataset = tf.data.Dataset.from_tensor_slices(image_paths)
    dataset = dataset.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(1)
    return dataset

calibration_data_dir = 'calibration_rice'
calibration_dataset = load_dataset(calibration_data_dir)

def transform_fn(data_item):
    return data_item.numpy()

nncf_dataset = nncf.Dataset(calibration_dataset, transform_fn)

# Load the TensorFlow model
# model = tf.saved_model.load("rice_model")
model = ov.Core().read_model("final_IR/cucumber_model.xml", "final_IR/cucumber_model.bin")

quantized_model = nncf.quantize(model, nncf_dataset)

# tf.saved_model.save(quantized_model, "quantized_rice_model")

# compile the model to transform quantized operations to int8
# model_int8 = ov.compile_model(quantized_model)

# input_fp32 = ... # FP32 model input
# res = model_int8(input_fp32)

# # save the model  
ov.save_model(quantized_model, "quantized_tomato.xml")

print("Quantization complete. Model saved as")

# sample_input = np.random.rand(1, 256, 256, 3).astype(np.float32)
# output = quantized_model(sample_input)
# print("Inference on quantized model successful.")
# print("Output shape:", output.shape)