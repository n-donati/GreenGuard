from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dashboard.models import Greenhouse
from django.http import JsonResponse

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