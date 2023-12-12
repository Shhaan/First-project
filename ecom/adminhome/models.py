from django.db import models
from django.utils.text import slugify
from django.db.models import Count
from usermain.models import Users
# Create your models here.
class Brand(models.Model):
    brand_image = models.ImageField(upload_to='Brand/')
    brand_name = models.CharField(max_length=40)
    def __str__(self):
        return self.brand_name
    
class Category(models.Model):
    Category_image = models.ImageField(upload_to='Category/')
    Category_name = models.CharField(max_length=40) 
    def __str__(self):
        return self.Category_name
    
class Products(models.Model):
    STATUS_CHOICES = (
        ('sale', 'Sale'),
        ('out of stock', 'Out of stock'),
    )
    product_name = models.CharField(max_length=50)
    product_des = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user_gender  =  models.CharField(max_length=10)
    product_price = models.BigIntegerField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sale')
    tag = models.CharField(max_length=20,null=True,blank=True)
    slug     =       models.SlugField(unique=True,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.product_name
class product_image(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Products') 
    
    def __str__(self):
        
        return f"{self.product.product_name} - Image {self.pk}"
    
class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"Cart for {self.user.first_name if self.user else 'Guest'}"



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=False)
    country = models.CharField(max_length=100)
    created_at = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # subtotal
# class Orderitem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
# unit price