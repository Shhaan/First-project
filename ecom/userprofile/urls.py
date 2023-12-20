from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('user-<int:id>/edit/',views.profile_edit,name='profile-edit'),
    
    
]
