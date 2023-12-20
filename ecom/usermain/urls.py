from django.urls import path
from . import views

urlpatterns = [
    path('user-login/',views.user_login,name='login'),
    path('user-registration/',views.register,name='register'),
    path('user-registration/verification',views.verification,name='verification'),
    path('',views.home,name='home'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('products/', views.products, name='products'),
    path('products-detail/<str:product_slug>', views.products_detail, name='products-detail'),
    path('products-detail/<str:product_slug>/add-review', views.addreview, name='addreview'),
    
]
