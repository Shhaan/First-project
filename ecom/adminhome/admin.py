from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Products)
admin.site.register(product_image)
admin.site.register(Cart)

 