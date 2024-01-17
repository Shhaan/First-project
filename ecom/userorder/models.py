from django.db import models
from usermain.models import Users
from adminhome.models import *
from autoslug import AutoSlugField


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False, null=True)
    paid_amount = models.CharField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    slug = AutoSlugField(populate_from="first_name", max_length=50, unique=True)
    total = models.CharField(max_length=260)
    shipping_address = models.ForeignKey(
        "shipping_address", on_delete=models.SET_NULL, null=True, blank=True
    )
    PAYMENT_METHOD_CHOICES = (
        ("cash_on_delivery", "Cash on Delivery"),
        ("pay_by_wallet", "Wallet  payment"),
        ("paypal", "PayPal"),
    )

    is_deleted = models.BooleanField(default=False)

    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return "order for " + self.user.first_name + " |   Email :  " + self.user.email


class Orderitem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    sub_total = models.IntegerField()
    quantity = models.IntegerField(default=1)
    slug = AutoSlugField(populate_from="order", max_length=50, unique=True)
    shipping_option = models.ForeignKey(
        "Shipping", on_delete=models.CASCADE, null=True, blank=True
    )
    total = models.CharField(null=True)

    def __str__(self):
        return (
            " order item  for  "
            + self.order.user.first_name
            + "  product is  "
            + self.product.product_name
        )


class shipping(models.Model):
    shipping_name = models.CharField(max_length=50)
    shipping_price = models.IntegerField()
    des = models.CharField(max_length=150)

    def __str__(self):
        return self.shipping_name


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Tax(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class wallet(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=250, unique=True)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email + "'s Wallet"


class shipping_address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)

    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=False)
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} , {self.second_name} ,{self.address} ,{self.phone},{self.state},{self.district}, {self.postal_code}"


class CategoryOffer(models.Model):
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categoryoffer"
    )

    def __str__(self):
        return self.name
