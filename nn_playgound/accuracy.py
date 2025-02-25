import os
from openvino.runtime import Core
import numpy as np
import cv2
from sklearn.metrics import accuracy_score, confusion_matrix
from tqdm import tqdm

# Initialize OpenVINO Runtime
ie = Core()

# Load the model
model_xml = "final_IR/cucumber_model.xml"
model_bin = "final_IR/cucumber_model.bin"
model = ie.read_model(model=model_xml, weights=model_bin)
compiled_model = ie.compile_model(model=model, device_name="CPU")

# Get input and output layer names
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

def preprocess_image(image_path, input_size):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (input_size, input_size))
    image = image.transpose((2, 0, 1))  # HWC to CHW
    image = np.expand_dims(image, axis=0)
    return image

def predict(image):
    results = compiled_model([image])[output_layer]
    return np.argmax(results, axis=1)[0]

def test_accuracy(test_dir, class_names):
    input_size = input_layer.shape[2]  # Assuming square input
    true_labels = []
    predicted_labels = []

    for class_name in class_names:
        class_dir = os.path.join(test_dir, class_name)
        for image_name in tqdm(os.listdir(class_dir), desc=f"Processing {class_name}"):
            image_path = os.path.join(class_dir, image_name)
            preprocessed_image = preprocess_image(image_path, input_size)
            prediction = predict(preprocessed_image)
            
            true_labels.append(class_names.index(class_name))
            predicted_labels.append(prediction)

    accuracy = accuracy_score(true_labels, predicted_labels)
    conf_matrix = confusion_matrix(true_labels, predicted_labels)

    print(f"Accuracy: {accuracy:.4f}")
    print("Confusion Matrix:")
    print(conf_matrix)

    return accuracy, conf_matrix

# Example usage
test_directory = "Rice_Leaf_AUG/test"  # Replace with your actual test directory
class_names = ['Bacterial Leaf Blight', 'Brown Spot', 'Healthy Rice Leaf', 'Leaf Blast', 'Leaf Scald', 'Sheath Blight']  # Replace with your actual class names

accuracy, conf_matrix = test_accuracy(test_directory, class_names)