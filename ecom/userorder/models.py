from django.db import models
from usermain.models import Users
from adminhome.models import *
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=False)
    country = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False,null=True)
    paid_amount = models.BigIntegerField(null=True,blank = True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return 'order for ' + self.user.first_name + ' |   Email :  ' + self.user.email
class Orderitem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    sub_total    = models.IntegerField()
    quantity =models.IntegerField(default = 1)
    def __str__(self)  :
        return ' order item  for  ' + self.order.user.first_name + '  product is  ' + self.product.product_name
