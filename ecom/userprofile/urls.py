from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('user-<int:id>/edit/',views.profile_edit,name='profile-edit'),
    path('order-details/',views.user_order,name='user-order'),
    path('order-details/track-order/<int:id>',views.check_detail,name='check-detail'),
    path('order-details/delete-order/<int:id>',views.delete_order,name='delete-order'),


    
    
    
]
