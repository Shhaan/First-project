from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(shipping)
admin.site.register(Coupon)
admin.site.register(shipping_address)
admin.site.register(Tax)
admin.site.register(CategoryOffer)

admin.site.register(wallet)
