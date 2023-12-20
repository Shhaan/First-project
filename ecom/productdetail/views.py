from adminhome.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from usermain.models import Users
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.db.models import *
import random
from django.contrib.auth.decorators import login_required
# Create your views here.
def category(request,category_name):
    if  request.user.is_authenticated == False:
        return redirect('usermain:login')
    
    products = Products.objects.prefetch_related('product_image_set').filter(Q(category__Category_name = category_name)& Q(is_deleted = False)& Q(brand__is_deleted = False)& Q(category__is_deleted = False))
    category = Category.objects.annotate(num_products=Count('products')).filter(Q(num_products__gt=0)&Q(is_deleted = False))
    
    brands = Brand.objects.annotate(num_products=Count('products')).filter(Q(num_products__gt=0)&Q(is_deleted = False))
    user_cart = Cart.objects.filter(user=request.user)
    
    total = 0  
        
    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price 
   
    context = {'category': category,'brands':brands,'products':products,'user_cart': user_cart,'total':total}

    return render(request,'productdetail/category.html',context)
    
def brand(request,brand_name):
    if  request.user.is_authenticated == False:
        return redirect('usermain:login')
    
    products = Products.objects.prefetch_related('product_image_set').filter(Q(brand__brand_name = brand_name)& Q(is_deleted = False)& Q(brand__is_deleted = False)& Q(category__is_deleted = False))
    category = Category.objects.annotate(num_products=Count('products')).filter(Q(num_products__gt=0)&Q(is_deleted = False))
    
    brands = Brand.objects.annotate(num_products=Count('products')).filter(Q(num_products__gt=0 )&Q(is_deleted = False))

    user_cart = Cart.objects.filter(user=request.user)
    
    total = 0  
        
    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price 

        
    context = {'category': category,'brands':brands,'products':products,'user_cart': user_cart,'total':total}
    return render(request,'productdetail/brand.html',context)