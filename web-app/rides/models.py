from django.db import models
from django.contrib.auth.models import User
# Create your models here.
statusChoice = [('open', 'open'), ('confirmed', 'confirmed'), ('complete', 'complete')]
class Ride(models.Model):
    # status = models.ChoiceField(choices=statusChoice)
    ride_id = models.AutoField(primary_key=True,unique=True)
    status = models.CharField(max_length=100, default="open")
    destination = models.CharField(max_length=100)
    arrival = models.TimeField()
    number = models.IntegerField(default=0)
    shared = models.BooleanField(default=False)
    user = models.IntegerField()
    driver = models.IntegerField(default=0)
    sharer = models.IntegerField(default=0)
    email = models.CharField(max_length=100, default="xxx@163.com")

# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    plate = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    passengers = models.IntegerField(default=0)