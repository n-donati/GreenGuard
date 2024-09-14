from django.shortcuts import render

# Create your views here.
def dashboard(request):
  return render(request, "dashboard.html", {})

def greenhouses(request):
  return render(request, "greenhouses.html", {})

def monitoring(request):
  return render(request, "monitoring.html", {})

def signup(request):
  return render(request, "signup.html", {})

def user_login(request):
  return render(request, "login.html", {})

def logout(request):
  return render(request, "logout.html", {})