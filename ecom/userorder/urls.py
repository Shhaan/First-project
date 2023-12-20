from django.urls import path
from . import views


urlpatterns = [
    path('<str:slug>/checkout/',views.checkout,name='checkout'),
    path('<str:slug>/chekout-pr-detail/',views.chekout_pr_in,name='chekout-pr-detail'),
    path('<str:slug>/shipping/',views.shipping,name='shipping'),
    

]