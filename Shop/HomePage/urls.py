from django.urls import path
from HomePage import views
from django.conf import settings
from django.conf.urls.static import static

app_name='HomePage'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/catalogue/', views.catalogue, name='catalogue'),
    path('user/catalogue/<int:product_id>/', views.singleProductPage, name='singleProductPage'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)