from django.db import models
from django.contrib.auth.models import User

class Greenhouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    crop_type = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.name} - {self.user.username}"