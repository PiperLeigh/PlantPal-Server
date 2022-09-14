from django.db import models

class SunType(models.Model):
    label = models.CharField(max_length=50)