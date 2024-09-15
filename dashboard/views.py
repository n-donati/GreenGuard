from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Greenhouse
import json

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
    elif request.session.get('is_guest'):
        user = AnonymousUser()
    else:
        return redirect('login')
    
    return render(request, "dashboard.html", {'user': user})

@login_required
def greenhouses(request):
    if request.method == "POST":
        selections = json.loads(request.POST.get('selections', '[]'))
        crop_type = request.POST.get('type', '')
        greenhouse = Greenhouse(
            user=request.user,
            name=f"Greenhouse {Greenhouse.objects.filter(user=request.user).count() + 1}",
            data=selections,
            crop_type=crop_type
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

@login_required
def monitoring(request):
    greenhouses = Greenhouse.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'greenhouses': json.dumps([{
            'id': gh.id,
            'name': gh.name,
            'crop_type': gh.crop_type,
            'data': gh.data
        } for gh in greenhouses])
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

