import openvino.runtime as ov
import numpy as np
from PIL import Image
import io

core = ov.Core()
# core.set_property("CPU", {"CONFIG_FILE": "./dashboard/NN_models/openvino_config.xml"})
model = core.read_model("quantized_model.xml")
compiled_model = core.compile_model(model, "CPU")
# Get input and output layers
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

def preprocess_image(image_data, target_size=(256, 256)):
    # Open the image using PIL
    img = Image.open(io.BytesIO(image_data))

    # Resize the image
    img = img.resize(target_size)

    # Convert to numpy array and normalize
    img_array = np.array(img).astype(np.float32)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    print(img_array.shape)

    return img_array

def serve_rice(image_data):
    preprocessed_img = preprocess_image(image_data)

    results = compiled_model([preprocessed_img])[output_layer]
    print("Results shape:", results.shape)
    print("Results content:", results)

    class_names = ["Bacterial Leaf Blight", "Brown Spot", "Healthy Rice Leaf", "Leaf Blast", "Leaf scald", "Sheath Blight"]
    predicted_class = class_names[np.argmax(results)]
    confidence = np.max(results)

    return {
        "predicted_class": predicted_class,
        "confidence": float(confidence),
        "raw_results": results.tolist()
    }

print(serve_rice(open("Rice_Leaf_AUG/Leaf Blast/aug_0_3.jpg", "rb").read()))
