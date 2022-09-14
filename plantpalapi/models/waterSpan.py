from django.db import models

class WaterSpan(models.Model):
    label = models.CharField(max_length=50)