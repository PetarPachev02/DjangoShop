from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from HomePage.models import Product
from .models import OrderLine , Order
from .cart import Cart
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from decimal import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from HomePage import *


@require_POST
def cartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = cartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cartDetail')
    
    
def cartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cartDetail')    
    
def cartDetail(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart,
                                          } )   

def purchase(request):
    if request.user.is_authenticated:
        if request.POST:
            cart = Cart(request)
            product = Product.objects.all()
            orderTotal = Decimal(request.POST.get('cart.get_total_price'))
            my_order = Order.objects.create(user=request.user, total=orderTotal)
            i=0
            for product in cart:
                product_id = int(request.POST.get('product.id.{}'.format(i)))
                product_quantity = int(request.POST.get('product.quantity.{}'.format(i)))
                i+=1
                product_price = request.POST.get('product.price')
                product_obj = Product.objects.get(id=product_id)
                orderTotal = Decimal(request.POST.get('cart.get_total_price'))
                my_orderLine = OrderLine.objects.create(user=request.user , order=my_order , product=product_obj, quantity=product_quantity)
                my_orderLine.save()
    
            my_order.save()
            cart.clear()
        return redirect('cart:cartDetail')
        
    else:
        return HttpResponse('You have to register first')
        
@login_required
def pastOrders(request , user_id):
    user_id = request.user.id
    user = request.user
    page = request.GET.get('page', 1)
    orderList = Order.objects.filter(user=user)
    paginator = Paginator(orderList, 10)
    
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orderss = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        
    context = {
                'orders': orders
              }
    
    return render(request , 'pastorders.html' , context)
    
def orderSinglePage(request, order_id ):
    myOrder = Order.objects.get(id=order_id)
    myOrderLine = OrderLine.objects.filter(order=myOrder)
    return render(request , 'singleorderview.html' , { 'myOrderLine' : myOrderLine,  
                                                       'myOrder' : myOrder   
                                                     })    
                                                                        
def orderRemove(request, order_id):
    user_id = request.user.id
    order = Order(request)
    order = Order.objects.filter(id=order_id)
    order.delete()
    return redirect('cart:pastOrders' , user_id)