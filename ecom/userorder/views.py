from django.shortcuts import render
from adminhome.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Order,Orderitem,shipping
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache ,cache_control

from django.db.models import *
# Create your views here.


@never_cache 
def chekout_pr_in(request,slug):
    if  request.user.is_authenticated == False :
        return redirect('usermain:login')
     
    if request.method =="POST":
       
       input_val  = request.POST['value']
       
       request.session['input_value'] = input_val.strip()
       
       return redirect(reverse('userorder:checkout', kwargs={'slug': slug}))
@never_cache  
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def checkout(request,slug):
    if  request.user.is_authenticated == False :
        
    
        return redirect('usermain:login')
    error = {}
     
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
            request.session['first_name'] = f_name
            request.session['last_name'] = l_name
            request.session['Address'] = Address
            request.session['postal_code'] = postalcode
            request.session['state'] = state    
            request.session['phone'] = phone    
            request.session['country'] = country    
            
            order = Order.objects.create(
                user=user, first_name=f_name, last_name=l_name, address=Address,
                postal_code=postalcode, state=state, phone=phone, country=country
            )
            request.session['order'] = order.id
            user_cart = Cart.objects.filter(user=request.user, product=product)
            
            quantity = 0
            for i in user_cart:
                total = i.product.product_price *i.quantity
                quantity =i.quantity

            input_val = request.session.get('input_value', '')
            if input_val is not None:
                input_val.strip()
            if    quantity !=0 or not input_val:
                if quantity == 0:
                    return redirect(reverse('userorder:shipping', kwargs={'slug': slug}))
                o_t = Orderitem.objects.create(order=order, product=product, quantity=quantity, sub_total=total)
                Cart.objects.filter(user=request.user, product=product).delete()
                request.session['input_value'] = None
                request.session['o_t'] = o_t.id
                
            else:
                total = int(input_val) * product.product_price
                o_t =Orderitem.objects.create(order=order, product=product, quantity=input_val, sub_total=total)
                request.session['input_value'] = None
                request.session['o_t'] = o_t.id

            return redirect(reverse('userorder:shipping', kwargs={'slug': slug}))

    
    
    context = {'product':product,'errors':error,}
    return render(request,'userorder/checkout.html',context)
@never_cache
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='usermain:login')
def  shippin(request,slug):
    product = Products.objects.get(slug = slug)
    order_id = request.session['o_t']
    order = Orderitem.objects.get(id = order_id)
    ship = shipping.objects.all()
    context = {'product':product,'ship':ship,'order':order}       
    return render(request,'userorder/shipping.html',context)
@login_required(login_url='usermain:login')
def  shippin_add(request,slug):
    if request.method == 'POST':
        shipp = request.POST.get('shipping')
        obj = shipping.objects.get(shipping_name=shipp)
        Orderitem.objects.filter(id = request.session['o_t']).update(shipping_option = obj)
    return redirect(reverse('userorder:payment-detail' ,kwargs={'slug':slug})) 
def payment_detail(request,slug):
    product = Products.objects.get(slug = slug)
    order_id = request.session['o_t']
    if request.method == 'POST':
        payment = request.POST.get('payment')
        total = request.POST.get('total')
        
        id = request.session['order']
        Order.objects.filter(id = id).update(payment_method = payment) 
        Orderitem.objects.filter(id = order_id).update(total =total )
        return redirect('usermain:home')   
    
    order = Orderitem.objects.get(id = order_id)
 
    context = {'product':product,'order':order}       
    return render(request,'userorder/payment.html',context)
