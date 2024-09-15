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
    BacterialLeafBlight = models.FloatField()
    BrownSpot = models.FloatField()
    Healthy = models.FloatField()
    LeafBlast = models.FloatField()
    LeafScald = models.FloatField()
    SheathBlight = models.FloatField()
    
    def __str__(self):
        return f"Rice - {self.greenhouse.name}"
  
class Tomato(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    BacterialSpot = models.FloatField()
    EarlyBlight = models.FloatField()
    Healthy = models.FloatField()
    LateBlight = models.FloatField()
    LeafMold = models.FloatField()
    SeptoriaLeafSpot = models.FloatField()
    SpiderMites = models.FloatField()
    TargetSpot = models.FloatField()
    TomatoMosaicVirus = models.FloatField()
    YellowLeafCurlVirus = models.FloatField()
    
    def __str__(self):
        return f"Tomato - {self.greenhouse.name}"
  
class Cucumber(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    Anthracnose = models.FloatField()
    BacterialWilt = models.FloatField()
    DownyMildew = models.FloatField()
    Healthy = models.FloatField()
    GummyStemBlight = models.FloatField()
    
    def __str__(self):
        return f"Cucumber - {self.greenhouse.name}"
    