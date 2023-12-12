from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login ,authenticate,logout
from django.contrib import messages
from .models import *
from usermain.models import Users
from django.db.models import *
# Create your views here.
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminhome:admin_panel')
    if request.method == 'POST':
        email = request.POST['Email-log']
        password = request.POST['Password-log']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('adminhome:admin_panel')  # Replace with your actual home URL
        else:
            messages.info(request, 'Enter a valid user')
            return redirect('adminhome:admin_login')
    return render(request,'adminhome/Login.html')
def admin_panel(request):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')
    
    order = Order.objects.count()
    context = {'order':order}
    return render(request,'adminhome/dashbord.html',context)
def admin_logout(request):
    logout(request)
    return redirect('adminhome:admin_login')

def customer(request):
    
    
    search = request.GET.get('search','')
    
    if search:
        customer = Users.objects.filter(Q(first_name__icontains=search) | Q(email__icontains=search) | Q(Number__icontains=search),Q(is_superuser=False))
    else:
        
        customer = Users.objects.filter(is_superuser=False)
    
    
    context = {'customer':customer}
    return render(request,'adminhome/customer.html',context)



def unblock_user(request,user_id):
    
    Users.objects.filter(id = user_id).update(is_blocked = False)
    
    
    return redirect(reverse('adminhome:customer'))

def block_user(request,user_id):
    Users.objects.filter(id = user_id).update(is_blocked = True)
    return redirect(reverse('adminhome:customer'))
