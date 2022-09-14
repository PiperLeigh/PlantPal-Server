from django.db import models
from .plantPalUser import PlantPalUser

class Swap(models.Model):
    coverPhoto = models.ImageField(
        upload_to='coverphotos', height_field=None,
        width_field=None, max_length=None, null=True)
    host = models.ForeignKey(PlantPalUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=300)
    attendees = models.ManyToManyField("PlantPalUser", related_name='swaps')