from django.shortcuts import render,redirect
from django.contrib.auth import login ,authenticate
from django.contrib import messages

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
    
    return render(request,'adminhome/dashbord.html')