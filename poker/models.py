from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
    picture = models.FileField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)
    

