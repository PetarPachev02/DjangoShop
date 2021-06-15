from django.shortcuts import render,redirect
from django.http import HttpResponse , Http404
from .models import Product
from django.shortcuts import get_object_or_404, render
from .forms import UserProfileInfoForm , UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from cart.forms import cartAddProductForm
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Guest'
    context = { 'username' : username }    
    return render(request, 'homepage.html' , context)

def catalogue(request):
    latest_products_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(latest_products_list, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context = {
               'products' : products
              }
    return render(request, 'catalogue.html', context )  

def singleProductPage(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_product_form = cartAddProductForm()
    return render(request, 'singleProductPage.html', {'product': product , 'cart_product_form': cart_product_form })

    
@login_required
def userLogout(request):
    your_data = request.session.get('your_key', None)
    current_expiry = request.session.get('_session_expiry')
    logout(request)
    if your_data:
        request.session['your_key'] = your_data
        if current_expiry:
           request.session['_session_expiry'] = current_expiry
    return render(request, 'loggedout.html')
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return render(request, 'logged-in.html')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})
   
   
   
   

