from django.contrib import admin
from django.utils.datetime_safe import datetime
from .models import Product
from .models import UserProfileInfo, User 

admin.site.register(Product) 
admin.site.register(UserProfileInfo) 

