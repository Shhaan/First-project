from adminhome.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Users
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.db.models import *
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django_otp.plugins.otp_totp.models import TOTPDevice
# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('usermain:home')
    if request.method == 'POST':
        email = request.POST['Email-log']
        password = request.POST['Password-log']
        user = authenticate(request, email=email, password=password)

        if user is not None :
            login(request,user)
            return redirect('usermain:home')  # Replace with your actual home URL
        else:
            messages.info(request, 'Enter a valid user')
            return redirect('usermain:login')
        
    return render(request,'usermain/Login.html')

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    error = {}
    if request.method == 'POST':
        First_name = request.POST['Firstname']
        Second_name = request.POST['Secondname']
        Number = request.POST.get('Number')
        Email = request.POST['Email']
        Gender = request.POST.get('Gender',None)
        Address = request.POST['Address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        Email_exist = Users.objects.filter(email = Email).exists()
        
        if password1 != password2:
            error['password_match'] = 'Both passwords must be the same'
        elif len(password1) <= 8:
            error['password1'] = 'Password must be at least 8 characters'

        if not First_name:
            error['First_name'] = 'First name must be entered'

        if Number is None or not Number:
            error['Number'] = 'Number must be entered'
        else:
            Number_exist = Users.objects.filter(Number=Number).exists()
            if Number_exist:
                error['Number'] = 'Number has been taken'
            elif len(str(Number)) != 10  :
                error['Number'] = 'Number Must be ten digits'

        if not Email:
            error['Email'] = 'Email must be entered'
        elif Email_exist:
            error['Email'] = 'Email has been taken'

        if not Address:
            error['Address'] = 'Address must be entered'

        if not error:
            # Continue with user registration...
           user = Users.objects.create_user(
                first_name=First_name,
                last_name=Second_name,
                Number=Number,
                email=Email,
                Gender=Gender,
                Address=Address,
                password=password1
            )
           
           otp = generate_otp()

           TOTPDevice(user=user, confirmed=True).save()
        
           user.otp = otp
           user.save()
           
           
         

           subject = 'OTP Verification'
           message = f'Your OTP is: {otp}'
           from_email = 'shanmohamme.123@gmail.com'
           to_email = [user.email]

           send_mail(subject, message, from_email, to_email)
           
           user = authenticate(request, email=Email, password=password1)
           
           if user is not None:
                login(request, user)
                url_success = reverse('usermain:verification')
                return redirect(url_success) 
        
    return render(request, 'usermain/Signup.html', {'errors': error})
@login_required
def verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp').strip()

        try:
            user = request.user 
            if user.otp == entered_otp:      
                url = reverse('usermain:home')
                return redirect(url)
            else:
                messages.info(request,'Enter correct otp')
                return redirect(reverse('usermain:verification'))

        except :   
            return redirect(reverse('usermain:verification'))

    return render(request, 'usermain/Verification.html')
def home(request):
    if  request.user.is_authenticated == False:
        return redirect('usermain:login')
    else:
        products = Products.objects.prefetch_related('product_image_set').filter(tag__startswith='T')
        category = Category.objects.all()
        brand = Brand.objects.filter()[:5]
        brands = Brand.objects.all()
        user_cart = Cart.objects.filter(user=request.user)
        
        
        
        context = {'category': category,'brands':brands, 'brand': brand,'products':products,'user_cart': user_cart}
        return render(request, 'usermain/Home.html', context)

def add_cart(request):
    
    if request.method == 'POST':
        num_product = int(request.POST['num_product'])
        product_name =request.POST['product_name']
        user = request.user
        product = Products.objects.get(product_name=product_name)
        cart_exist = Cart.objects.filter(user=user,product=product).exists()
        if cart_exist:
            Cart.objects.filter(user=user,product=product).update(quantity = F('quantity')+num_product)
        else:
             
            Cart.objects.create(user=user,product=product,quantity = num_product)
        
    
            
            
        return redirect(request.META.get('HTTP_REFERER', 'usermain:home'))
       
def update_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        product_id = request.POST.get('product_edit_id')
        edit_quantity = request.POST.get('edit-count')
        Cart.objects.filter(user=request.user,product__id=product_id).update(quantity=edit_quantity)

        return redirect(request.META.get('HTTP_REFERER', 'usermain:home'))
def delete_cart(request):
    if request.method =="GET":
        product_id = request.GET.get('product_delete_id')
        if request.user.is_authenticated:
          
            Cart.objects.get(product__id=product_id, user=request.user).delete()

            return redirect(request.META.get('HTTP_REFERER', 'usermain:home'))

def products(request):
    if  request.user.is_authenticated == False:
        return redirect('usermain:login')
    else:
        products = Products.objects.prefetch_related('product_image_set').all()
        category = Category.objects.all()
       
        brands = Brand.objects.all()
        user_cart = Cart.objects.filter(user=request.user)
        
        
        context = {'category': category,'brands':brands,'products':products,'user_cart': user_cart}
    return render(request,'usermain/products.html',context)
def products_detail(request,product_slug):
    product = Products.objects.get(slug =product_slug)
    user_cart = Cart.objects.filter(user=request.user)
    category = Category.objects.all()
    related_product = Products.objects.filter(Q(category=product.category)|Q(brand = product.brand)).exclude(id=product.id)
    brands = Brand.objects.all()
    context = {'product':product,'user_cart': user_cart,'category': category,'brands':brands,'relate':related_product}

    return render(request,'usermain/product-detail.html',context)