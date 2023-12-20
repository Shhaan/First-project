from django.shortcuts import render
from adminhome.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from usermain.models import Users,Review
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.db.models import *
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,authenticate,logout
from django.views.decorators.cache import never_cache




# Create your views here.
def profile(request): 
    if  request.user.is_authenticated == False:
        return redirect('usermain:login') 
    user_cart = Cart.objects.filter(user=request.user).order_by('-id')
    
    total = 0  
    
    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    user = request.user
    context = {'user_cart': user_cart,'total':total,'user':user}
    return render(request,'userprofile/profile.html',context)
def user_logout(request):
    
    logout(request)
    
    return redirect('usermain:login')
def profile_edit(request,id):
    if  request.user.is_authenticated == False:
        return redirect('usermain:login') 
    errors ={}
    if request.method == 'POST':
        f_name = request.POST.get('first_name').strip()
        l_name = request.POST['last_name']
        gender = request.POST['gender']
        number = request.POST['number']
        email = request.POST['email']
        address = request.POST.get('address').strip()
        email_exist = Users.objects.exclude(id=id).filter(email  = email).exists()
        number_exist = Users.objects.exclude(id=id).filter(Number  = number).exists()
        if not f_name:
            errors['f_name'] = 'Enter First name'
        if not number:
            errors['number'] = 'Enter Number'
        if not address:
            errors['address'] = 'Enter Address'  
        if not email:
            errors['email'] ='Enter email'
        if  email_exist:
            errors['email_exist'] ='Email already taken'
        if  number_exist:
            errors['number_exist'] ='Number already taken'   
        if not errors:
            Users.objects.filter(id = id).update(first_name = f_name,last_name = l_name,Number = number,Address = address,email = email,Gender= gender)
            return redirect(request.META.get('HTTP_REFERER' ))
   
    user_cart = Cart.objects.filter(user=request.user).order_by('-id')
    
    total = 0  
    
    for i in user_cart:
        total += i.quantity * i.product.product_price

    user = request.user
    context = {'user_cart': user_cart,'total':total,'errors':errors }
        
    return render(request,'userprofile/profile-edit.html',context)