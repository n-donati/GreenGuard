import numpy as np
from openvino.runtime import Core
from PIL import Image

# Initialize OpenVINO Runtime
ie = Core()

# Load the IR model (replace 'model.xml' with your model path)
model = ie.read_model(model="quantized_model.xml")
compiled_model = ie.compile_model(model=model, device_name="CPU")

# Get input and output layers
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)
input_shape = input_layer.shape()

# Preprocess the image
def preprocess_image(image_path, input_shape):
    image = Image.open(image_path).convert('RGB')
    resized_image = image.resize((input_shape[3], input_shape[2]))
    image_array = np.array(resized_image)
    image_array = image_array.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array.astype(np.float32)  # Convert to FP32
    return image_array

# Replace 'path_to_your_image.jpg' with the actual image you want to test
input_image = preprocess_image('Rice_Leaf_AUG/Leaf Blast/aug_0_3.jpg', input_shape)

# Perform inference
result = compiled_model([input_image])[output_layer]

# Post-process the output
predicted_class = np.argmax(result, axis=1)[0]
print(f"Predicted class index: {predicted_class}")
