from django.shortcuts import render
from adminhome.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Order,Orderitem
from django.contrib import messages

from django.views.decorators.cache import never_cache ,cache_control

from django.db.models import *
# Create your views here.

input_val = None
@never_cache 
def chekout_pr_in(request,slug):
    if  request.user.is_authenticated == False :
        return redirect('usermain:login')
    global input_val
    if request.method =="POST":
       
       input_val  = request.POST['value']
       
       return redirect(reverse('userorder:checkout', kwargs={'slug': slug}))
@never_cache  
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def checkout(request,slug):
    if  request.user.is_authenticated == False :
        
    
        return redirect('usermain:login')
    error = {}
    global input_val
    product = Products.objects.get(slug = slug)
    if request.method == 'POST':
        
        f_name = request.POST.get('f_name').strip()
        l_name = request.POST.get('l_name').strip()
        phone = request.POST['phone']
        Address = request.POST.get('Address').strip()
        country = request.POST.get('country').strip()
        state = request.POST.get('state').strip()
        postalcode = request.POST.get('postalcode').strip()
        user = request.user
        if not f_name:
            
            error['First_name'] = 'First name must be entered'
        if not l_name:
            error['last_name'] = 'Last name must be entered'

        if   not phone:
            error['Number'] = 'Number must be entered'


        if not country:
            error['country'] = 'country must be entered'
        if not state:
            error['state'] = 'state must be entered'
        if not postalcode:
            error['postalcode'] = 'postalcode must be entered'

        if not Address:
            error['Address'] = 'Address must be entered'


        if not error:
           order = Order.objects.create(user = user,first_name =f_name,last_name=l_name,address=Address,postal_code=postalcode,state=state,phone=phone,country=country)
           
           user_cart = Cart.objects.filter(user=request.user ,product = product)
    
           total = 0  
                
           for cart_item in user_cart:
                total += cart_item.quantity * cart_item.product.product_price 
                 
                qua = cart_item.quantity
           
           if input_val == None :
                
                Orderitem.objects.create(order = order,product = product,quantity = qua,sub_total = total)
                Cart.objects.filter(user=request.user,product=product).delete()
                input_val = None
           else:
               t = int(input_val) * product.product_price
               Orderitem.objects.create(order = order,product = product,quantity = input_val,sub_total = t)
               input_val = None
           
           return redirect(reverse('userorder:shipping',kwargs={'slug': slug}))
    
    
    context = {'product':product,'errors':error}
    return render(request,'userorder/checkout.html',context)
@never_cache
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def  shipping(request,slug):
    product = Products.objects.get(slug = slug)
    context = {'product':product}       
    return render(request,'userorder/shipping.html',context)
    
 

