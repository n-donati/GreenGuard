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
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from api.models import *

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
        bins = ['Anthracnose', 'Bacterial Wilt', 'Downy Mildew', 'Fresh Leaf', 'Gummy Stem Blight']
      elif crop_type == 'rice':
        client = make_grpc_client('34.123.59.235:9000')
        model_name = 'rice_model'
        bins = ['Bacterial Leaf Blight', 'Brown Spot', 'Healthy Rice Leaf', 'Leaf Blast', 'Leaf Scald', 'Sheath Blight']
      elif crop_type == 'tomato':
        client = make_grpc_client('34.123.59.235:8000')
        model_name = 'tomato_model'
        bins = ['Bacterial Spot', 'Early Blight', 'Healthy Tomato Leaf', 'Late Blight', 'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites', 'Target Spot', 'Tomato Mosaic Virus', 'Yellow Leaf Curl Virus']
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Greenhouse
import json
from dashboard.frida import recommendation1

# Create your views here.
def dashboard(request):
    request.session["user_id"] = request.user.id 
    if request.user.is_authenticated:
        user = request.user
    elif request.session.get('is_guest'):
        user = AnonymousUser()
    else:
        return redirect('login')
    
    # extraer del database cantidad de invernaderos, salud general y ultima actualizacion
    
    # recommendation = recommendation1(10, 90, "2022-01-01")
    # greenhouses = Greenhouse.objects.filter(user=request.user)
    user_id = request.session["user_id"]
    greenhouses = list(Greenhouse.objects.filter(user=User.objects.get(id=user_id)))
    
    total_square_units = 0
    weighted_health_sum = 0
    
    # Iterate through all the greenhouses
    for greenhouse in greenhouses:
        square_units = greenhouse.total_square_units
        crop = None
        
        # Check which crop type the greenhouse has using related names
        if greenhouse.crop_type == "rice":
            crop = greenhouse.rice.first()
        elif greenhouse.crop_type == "tomato":
            crop = greenhouse.tomato.first()
        elif greenhouse.crop_type == "cucumber":
            crop = greenhouse.cucumber.first()

        if crop is not None and square_units:
            # Calculate the health percentage for the crop
            health_percentage = crop.healthy if crop.healthy is not None else 0
            health_percentage *= 100 
            
            if health_percentage is not None:
                weighted_health_sum += health_percentage * square_units
                total_square_units += square_units
    
    # Calculate overall weighted health percentage
    if total_square_units > 0 and crop is not None:
        salud_general = weighted_health_sum / total_square_units
    else:
        salud_general = 0  # Default if no square footage is available
    
    rating = 0
    
    return render(request, "dashboard.html", {'user': user, 'greenhouse_quantity':len(greenhouses), 'salud_general': salud_general, 'rating': rating})

def get_recommendation(request):
    porcentaje_salud = request.GET.get('salud_general', 90)
    user_id = request.session["user_id"]
    greenhouses = list(Greenhouse.objects.filter(user=User.objects.get(id=user_id)))
    
    last_submission_date = Image.objects.filter(user=User.objects.get(id=user_id)).order_by('-uploaded').first().uploaded

    recommendation = recommendation1(len(greenhouses), porcentaje_salud, last_submission_date)
    return JsonResponse({'recommendation': recommendation})

@login_required
def greenhouses(request):
    if request.method == "POST":
        selections = json.loads(request.POST.get('selections', '[]'))
        crop_type = request.POST.get('type', '')
        print(selections)
        greenhouse = Greenhouse(
            user=request.user,
            name=f"Greenhouse {Greenhouse.objects.filter(user=request.user).count() + 1}",
            data=selections,
            crop_type=crop_type, 
            total_square_units=sum((area['end']['x'] - area['start']['x'] + 1) * (area['end']['y'] - area['start']['y'] + 1) for area in selections)
        )
        greenhouse.save()
        return JsonResponse({"success": True})

    # Fetch data for the current user
    user_greenhouses = Greenhouse.objects.filter(user=request.user).order_by('-created_at')
    total_greenhouses = user_greenhouses.count()
    total_square_units = sum(sum((area['end']['x'] - area['start']['x'] + 1) * (area['end']['y'] - area['start']['y'] + 1) for area in greenhouse.data) for greenhouse in user_greenhouses)
    
    context = {
        'total_greenhouses': total_greenhouses,
        'total_square_units': total_square_units,
        'greenhouses': json.dumps([{'id': gh.id, 'name': gh.name, 'data': gh.data} for gh in user_greenhouses])
    }
    return render(request, "greenhouses.html", context)

@login_required
@require_http_methods(["POST"])
def edit_greenhouse_name(request, greenhouse_id):
    greenhouse = get_object_or_404(Greenhouse, id=greenhouse_id, user=request.user)
    new_name = request.POST.get('new_name')
    if new_name:
        greenhouse.name = new_name
        greenhouse.save()
        return JsonResponse({"success": True, "new_name": new_name})
    return JsonResponse({"success": False, "error": "Name cannot be empty"}, status=400)

@login_required
@require_http_methods(["POST"])
def delete_greenhouse(request, greenhouse_id):
    greenhouse = get_object_or_404(Greenhouse, id=greenhouse_id, user=request.user)
    greenhouse.delete()
    return JsonResponse({"success": True})

def greenhouse_to_dict(gh):
    gh_dict = model_to_dict(gh, fields=['id', 'name', 'crop_type'])
    gh_dict['data'] = gh.data  # Assuming 'data' is a JSONField or similar
    gh_dict['green'] = gh.images.exists()  # Efficiently check if images exist
    if gh.crop_type == "rice": 
      info = gh.rice
    elif gh.crop_type == "cucumber":
      info = gh.cucumber
    elif gh.crop_type == "tomato":
      info = gh.tomato
    print(info)
    return gh_dict

@login_required
def monitoring(request):
    greenhouses = Greenhouse.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'greenhouses': json.dumps([greenhouse_to_dict(gh) for gh in greenhouses], cls=DjangoJSONEncoder)
    }
    return render(request, "monitoring.html", context)

def signup(request):
    if request.method == 'POST':
        name = request.POST['signup-name']
        email = request.POST['signup-email']
        password = request.POST['signup-password']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')
    
    return render(request, "signup.html")

def user_login(request):
    if request.method == 'POST':
        email = request.POST['signin-email']
        password = request.POST['signin-password']
        remember_me = request.POST.get('RememberPassword', False)
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)  # Changed this line
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('dashboard')  # Redirect to dashboard page after login
        else:
            messages.error(request, 'Invalid email or password')
    else:
        # Add a guest login option
        if 'guest_login' in request.GET:
            request.session['is_guest'] = True
            return redirect('dashboard')
    
    return render(request, "login.html")



def logout(request):
    auth_logout(request)
    return redirect('home')

from django.http import JsonResponse

def get_greenhouse_data(request):
    greenhouse_id = request.GET.get('greenhouse_id')
    greenhouse = Greenhouse.objects.get(id=greenhouse_id)
    return JsonResponse({'data': greenhouse.data})

def orders(request):
    return render(request, "orders.html")