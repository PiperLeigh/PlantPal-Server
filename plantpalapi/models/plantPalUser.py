from django.db import models
from django.contrib.auth.models import User

class PlantPalUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(
        upload_to='profilepictures', height_field=None,
        width_field=None, max_length=None, null=True)
    address = models.CharField(max_length=100)
    bio = models.CharField(max_length=300)