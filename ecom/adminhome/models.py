from django.db import models

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
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='products/')
    product_des = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user_gender  =  models.CharField(max_length=10)
    product_price = models.BigIntegerField()
    quantity = models.IntegerField()
    status = models.BooleanField()
    tag = models.CharField(max_length=20)
    def __str__(self):
        return self.product_name