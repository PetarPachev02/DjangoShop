from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   portfolio_site = models.URLField(blank=True)
   profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
   address = models.CharField(max_length=200)

   def __str__(self):
    return self.user.username

class Product(models.Model):
   name = models.CharField(max_length=200)
   price = models.DecimalField(decimal_places=2, max_digits=10)
   image = models.ImageField(upload_to='static/images/' , blank=True)
   description = models.TextField()
   publish_date = models.DateField(default=timezone.now) 
   def __str__(self):
        return self.name

