import argparse
import numpy as np
from PIL import Image
from ovmsclient import make_grpc_client

def load_image_from_file(file_path):
    return Image.open(file_path)

def preprocess_image(image, target_size=(224, 224)):
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)

def main():
    parser = argparse.ArgumentParser(description='Classify rice leaf image using OpenVINO Model Server')
    parser.add_argument('--image', required=True, help='Path to the image file')
    parser.add_argument('--service_url', default='localhost:9000', help='URL to gRPC service')
    parser.add_argument('--model_name', default='rice_model', help='Model name to query')
    parser.add_argument('--model_version', default=0, type=int, help='Model version to query')
    args = parser.parse_args()

    image = load_image_from_file(args.image)
    preprocessed_image = preprocess_image(image)

    client = make_grpc_client(args.service_url)

    inputs = {
        'keras_tensor': preprocessed_image
    }

    try:
        response = client.predict(inputs, args.model_name, args.model_version)

        print("Raw response:")
        print(response)
        print("\nResponse type:", type(response))
        
        if isinstance(response, dict):
            for key, value in response.items():
                print(f"\nKey: {key}")
                print(f"Value type: {type(value)}")
                print(f"Value shape (if numpy array): {value.shape if isinstance(value, np.ndarray) else 'N/A'}")
                print(f"Value content: {value}")

        if 'output_0' in response:
            output = response['output_0']
            print("\nOutput type:", type(output))
            print("Output shape:", np.array(output).shape if hasattr(output, '__iter__') else "N/A")
            print("Output content:", output)
            
            class_names = ['Bacterial Leaf Blight', 'Brown Spot', 'Leaf Smut', 'Normal', 'Paddy Blast', 'Tungro']
            
            if isinstance(output, (list, np.ndarray)):
                output_array = np.array(output).flatten()  # Flatten in case it's 2D
                predicted_class = class_names[np.argmax(output_array)]
                confidence = np.max(output_array)

                print(f"\nPredicted class: {predicted_class}")
                print(f"Confidence: {confidence:.2f}")

                print("\nClass probabilities:")
                for name, prob in zip(class_names, output_array):
                    print(f"{name}: {prob:.4f}")
            else:
                print("\nUnable to process output. Unexpected format.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nModel metadata:")
        metadata = client.get_model_metadata(args.model_name, args.model_version)
        print(metadata)

if __name__ == "__main__":
    main()