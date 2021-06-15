from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='cart'

urlpatterns = [
    path('', views.cartDetail, name='cartDetail'),
    path('add/<int:product_id>/',views.cartAdd,name='cartAdd'),
    path('remove/<int:product_id>/',views.cartRemove,name='cartRemove'),
    path('pastorders/<int:user_id>/' , views.pastOrders , name='pastOrders'),
    path('purchase/' , views.purchase , name = 'purchase'),
    path('removeorder/<int:order_id>/' , views.orderRemove , name = 'orderRemove'),
    path('singleorder/<int:order_id>' , views.orderSinglePage , name = 'orderSinglePage')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)