from django.shortcuts import render, redirect
from dashboard.models import Image
from django.utils.text import get_valid_filename
import os
import requests
from io import BytesIO
import uuid
from django.core.files.storage import default_storage
import numpy as np
from PIL import Image as PILImage
from ovmsclient import make_grpc_client
def save_unique_file(file, folder=''):
  # Generate a unique filename
  original_name = get_valid_filename(file.name)
  name, ext = os.path.splitext(original_name)
  unique_filename = f"{name}_{uuid.uuid4().hex}{ext}"
  
  # Save the file with the unique name
  file_path = os.path.join(folder, unique_filename)
  file_name = default_storage.save(file_path, file)
  
  return file_name

def preprocess_image(image, target_size=(224, 224)):
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)

def convert_to_python_types(obj):
    if isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, (list, tuple)):
        return [convert_to_python_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_python_types(value) for key, value in obj.items()}
    return obj

def get_images(request): 
  if request.method == "POST": 
    images = request.FILES.getlist('images')
    predictions = []
    for image in images:
      path = save_unique_file(image)
      obj = Image(user=request.user, path=path)
      obj.save()
      file_url = default_storage.url(path)
      response = requests.get(file_url)
      open_image = PILImage.open(BytesIO(response.content))
      preprocessed_image = preprocess_image(open_image)
      # TODO remove ip address
      client = make_grpc_client('34.123.59.235:9000')
      inputs = {'keras_tensor': preprocessed_image}
      # TODO connect with external variable
      # TODO hide IP address
      crop_type = 'rice'
      if crop_type == 'cucumber': 
        model_name = 'cucumber_model'
        client = make_grpc_client('34.123.59.235:7000')
        bins = []
      elif crop_type == 'rice':
        client = make_grpc_client('34.123.59.235:9000')
        model_name = 'rice_model'
        bins = ['Bacterial Leaf Blight', 'Brown Spot', 'Healthy Rice Leaf', 'Leaf Blast', 'Leaf Scald', 'Sheath Blight']
      elif crop_type == 'tomato':
        client = make_grpc_client('34.123.59.235:8000')
        model_name = 'tomato_model'
        bins = []
      model_version = 0
      response = client.predict(inputs, model_name, model_version)
      output = response
      if isinstance(output, (list, np.ndarray)):
        output_array = np.array(output).flatten()  # Flatten in case it's 2D
        predicted_class = bins[np.argmax(output_array)]
        confidence = np.max(output_array)
      tup = (predicted_class, confidence)
      print(tup)
      predictions.append((predicted_class, confidence))
    request.session['prediction'] = convert_to_python_types(predictions)
    return redirect('get_images')
  return render(request, 'get_images.html', {"predictions": request.session['prediction'] if request.session.get('prediction') else None})