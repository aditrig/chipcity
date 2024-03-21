from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    last_name   = models.CharField(max_length=30)
    first_names = models.CharField(max_length=30)
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
    picture = models.FileField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)
    wallet = models.DecimalField(max_digits = 6, decimal_places = 2)
    
class Leger(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
    pot = models.DecimalField(max_digits=10, decimal_places=2)
    table_num = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_num')

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='participant')
    leger = models.ForeignKey(Leger, on_delete=models.PROTECT, related_name='table_num')
    money_in_hand = models.DecimalField(max_digits=10, decimal_places=2, help_text="Money this user has in hand for this game")
    first_card = models.CharField(max_length=30)
    second_card = models.CharField(max_length=30)



