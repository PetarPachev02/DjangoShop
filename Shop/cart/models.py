from django.db import models
from django.contrib.auth.models import User
from HomePage.models import Product
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

class Order(models.Model):
    user = models.ForeignKey(User ,blank=True, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(decimal_places=2, max_digits=10 , null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
class OrderLine(models.Model):    
    user = models.ForeignKey(User,  blank=True, on_delete=models.CASCADE) 
    order = models.ForeignKey(Order, null=True , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self): return "This order line contains {} {}(s).".format(self.quantity, self.product.name) 
    
    
@receiver(post_save, sender=OrderLine) 
def update_order(sender, instance, **kwargs): 
    instance.order.count += instance.quantity
    instance.order.updated = datetime.now()
 


