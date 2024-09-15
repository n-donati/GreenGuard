from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dashboard.models import Greenhouse
from django.http import JsonResponse
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

@api_view(["POST"])
def delete(request, greenhouse_id):
  greenhouse = get_object_or_404(Greenhouse, id=greenhouse_id, user=request.user)
  greenhouse.delete()
  return Response({"success": True})

@api_view(["POST"])
def edit(request, greenhouse_id):
  greenhouse = get_object_or_404(Greenhouse, id=greenhouse_id, user=request.user)
  new_name = request.POST.get('new_name')
  if new_name:
      greenhouse.name = new_name
      greenhouse.save()
      return JsonResponse({"success": True, "new_name": new_name})
  return Response({"success":True})

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
@api_view(["POST"])
def upload_images(request):
   id = request.POST.get("greenhouseId")
   greenhouse = get_object_or_404(Greenhouse, id=id, user=request.user)
   crop_type = greenhouse.crop_type
   predictions = []
   images = request.FILES.getlist('images')
   for image in images:
    path = save_unique_file(image)
    obj = Image(user=request.user, path=path, greenhouse=greenhouse)
    obj.save()
   return Response({"success": True})