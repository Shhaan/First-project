from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from .models import Users
from django.contrib import messages
from django.contrib.auth import authenticate,login
# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['Email-log']
        password = request.POST['Password-log']
        user = authenticate(username=email, password=password)

        if user is not None :
            login(request)
            return redirect('home')  # Replace with your actual home URL
        else:
            messages.info(request, 'Enter a valid user')
            return redirect('login')
        
    return render(request,'Login.html')
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
            Number_exist = Users.object.filter(Number=Number).exists()
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
           user = Users.object.create_user(
                first_name=First_name,
                second_name=Second_name,
                Number=Number,
                email=Email,
                Gender=Gender,
                Address=Address,
                password=password1
            )
           
           url_success = reverse_lazy('verification')
           return redirect(url_success)  # Redirect to a success page
    
    return render(request, 'Signup.html', {'errors': error})
def verification(request):
    
    return render(request,'Verification.html')
def home(request):
    
    
    
    return render(request,'Home.html')