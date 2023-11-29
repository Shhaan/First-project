from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.admin_login,name='admin_login'),
    path('',views.admin_panel,name='admin_panel'),
 
]
