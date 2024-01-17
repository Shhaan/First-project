from django.urls import path
from . import views


urlpatterns = [
    path("<str:slug>/checkout/", views.checkout, name="checkout"),
    path(
        "<str:slug>/checkout-address/",
        views.checkout_shipping_address,
        name="checkout-with-shipping-adderss",
    ),
    path(
        "<str:slug>/chekout-pr-detail/", views.chekout_pr_in, name="chekout-pr-detail"
    ),
    path("<str:slug>/<str:ot>/<str:o>/shipping/", views.shippin, name="shipping"),
    path(
        "<str:slug>/<str:ot>/<str:o>/add-shipping-detail/",
        views.shippin_add,
        name="shipping-detail-add",
    ),
    path(
        "<str:slug>/<str:ot>/<str:o>/payment-detail/",
        views.payment_detail,
        name="payment-detail",
    ),
    path(
        "apply-coupon/<str:slug>/<str:ot>/<str:o>",
        views.apply_coupon,
        name="apply-coupon",
    ),
    path("cart-buy/checkout", views.bulk_buy, name="bulk-buy"),
    path("cart-buy/checkout-address", views.bulk_buy_address, name="bulk-buy-address"),
    path(
        "cart-buy/payment/<str:order_slug>/<str:o>",
        views.bulk_buy_payment,
        name="bulk-buy-payment",
    ),
    path("payment/payment-success/", views.payment_success, name="payment-success"),
    path(
        "payment/payment-success/cart",
        views.payment_success_cart,
        name="payment-success-bulk",
    ),
    path("payment/payment-failed/", views.payment_failed, name="payment-failed"),
    path(
        "apply-coupon-cart/<str:order_slug>/<str:o>",
        views.coupon_cart,
        name="apply-coupon-cart",
    ),
]
