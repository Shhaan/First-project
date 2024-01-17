from . import views
from django.urls import path

urlpatterns = [
    path("product/", views.product, name="products"),
    path(
        "product/unlist-product/<int:product_id>",
        views.unlist_product,
        name="unlist-product",
    ),
    path(
        "product/list-product/<int:product_id>", views.list_product, name="list-product"
    ),
    path("product/<int:product_id>/edit", views.edit_product, name="edit-product"),
    path("product/addproduct/", views.add_product, name="addproduct"),
    path("product/<int:product_id>/edit-image", views.edit_image, name="edit-image"),
    path("product/<int:img_id>/delete-image", views.delete_image, name="delete-image"),
    path("brand/", views.brand, name="brand"),
    path("brand/unlist-brand/<int:brand_id>", views.unlist_brand, name="unlist-brand"),
    path("brand/list-brand/<int:brand_id>", views.list_brand, name="list-brand"),
    path("brand/edit-brand/<int:brand_id>", views.edit_brand, name="edit-brand"),
    path("brand/addbrand/", views.add_brand, name="addbrand"),
    path("category/", views.category, name="category"),
    path(
        "category/unlist-category/<int:category_id>",
        views.unlist_category,
        name="unlist-category",
    ),
    path(
        "category/list-category/<int:category_id>",
        views.list_category,
        name="list-category",
    ),
    path(
        "category/edit-category/<int:category_id>",
        views.edit_category,
        name="edit-category",
    ),
    path("category/addcategory/", views.add_category, name="addcategory"),
    path("orders/", views.orders, name="orders"),
    path("orders/cancel-order/<int:id>", views.cancel_order, name="cancel-order"),
    path("orders/order-detail/<int:id>", views.order_detail, name="order-detail"),
    path("orders/change-status/<int:id>", views.change_status, name="change-status"),
    path("coupon/", views.coupon, name="coupon"),
    path("coupon/add-coupon", views.add_coupon, name="add-coupon"),
    path("coupon/edit-coupon/<int:coupon_id>", views.edit_coupon, name="edit-coupon"),
    path("coupon/list-coupon/<int:coupon_id>", views.list_coupon, name="list-coupon"),
    path(
        "coupon/unlist-coupon/<int:coupon_id>",
        views.unlist_coupon,
        name="unlist-coupon",
    ),
    path("tax/", views.tax, name="tax"),
    path("tax/add-tax", views.add_tax, name="add-tax"),
    path("tax/edit-tax/<int:tax_id>", views.edit_tax, name="edit-tax"),
    path("tax/list-tax/<int:tax_id>", views.list_tax, name="list-tax"),
    path("tax/unlist-tax/<int:tax_id>", views.unlist_tax, name="unlist-tax"),
]
