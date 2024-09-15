from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Image(models.Model): 
  path = models.CharField(max_length=200, null=False, default='')
  uploaded = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
  greenhouse = models.ForeignKey("Greenhouse", on_delete=models.CASCADE, null=True, related_name="images")
  
class Greenhouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    crop_type = models.CharField(max_length=100, default="")
    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Rice(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    bacterial_leaf_blight = models.FloatField(null=True)
    brown_spot = models.FloatField(null=True)
    healthy = models.FloatField(null=True)
    leaf_blast = models.FloatField(null=True)
    leaf_scald = models.FloatField(null=True)
    sheath_blight = models.FloatField(null=True)
    
    def __str__(self):
        return f"Rice - {self.greenhouse.name}"
  
class Tomato(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    bacterial_spot = models.FloatField(null=True)
    early_blight = models.FloatField(null=True)
    healthy = models.FloatField(null=True)
    late_blight = models.FloatField(null=True)
    leaf_mold = models.FloatField(null=True)
    septoria_leaf_spot = models.FloatField(null=True)
    spider_mites = models.FloatField(null=True)
    target_spot = models.FloatField(null=True)
    tomato_mosaic_virus = models.FloatField(null=True)
    yellow_leaf_curl_virus = models.FloatField(null=True)
    
    def __str__(self):
        return f"Tomato - {self.greenhouse.name}"
  
class Cucumber(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    anthracnose = models.FloatField(null=True)
    bacterial_wilt = models.FloatField(null=True)
    downy_wildew = models.FloatField(null=True)
    healthy = models.FloatField(null=True)
    gummy_stem_blight = models.FloatField(null=True)
    
    def __str__(self):
        return f"Cucumber - {self.greenhouse.name}"
