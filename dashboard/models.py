from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Image(models.Model): 
  path = models.CharField(max_length=200, null=False, default='')
  uploaded = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)