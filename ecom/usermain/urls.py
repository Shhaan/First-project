from django.urls import path
from . import views

urlpatterns = [
    path('user-login/',views.user_login,name='login'),
    path('user-registration/',views.register,name='register'),
    path('user-registration/verification',views.verification,name='verification'),
    path('',views.home,name='home'),


]
