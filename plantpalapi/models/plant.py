from django.db import models
from .waterSpan import WaterSpan
from .sunType import SunType
from datetime import date

class Plant(models.Model):
    plantPhoto = models.ImageField(
        upload_to='plantphotos', height_field=None,
        width_field=None, max_length=None, null=True)
    name = models.CharField(max_length=50)
    water = models.IntegerField(default=1)
    waterSpanId = models.ForeignKey(WaterSpan, on_delete=models.CASCADE)
    sunType = models.ForeignKey(SunType, on_delete=models.CASCADE)
    lastWatered = models.DateField(default=date.today)
    petToxic = models.BooleanField()
    notes = models.CharField(max_length=300)