from django.contrib import admin
from .models import OrderLine , Order
from .cart import Cart
from django.utils.datetime_safe import datetime

class OrderLineAdmin(admin.ModelAdmin):
    # Overide of the save model
    def save_model(self, request, obj, form, change):
        obj.order.total += obj.quantity * obj.product.price
        obj.order.count += obj.quantity
        obj.order.updated = datetime.now()
        obj.order.save()
        super().save_model(request, obj, form, change)

admin.site.register(OrderLine , OrderLineAdmin)
admin.site.register(Order)
