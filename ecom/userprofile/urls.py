from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("logout/", views.user_logout, name="logout"),
    path("user-<int:id>/edit/", views.profile_edit, name="profile-edit"),
    path("order-details/", views.user_order, name="user-order"),
    path("wallet/", views.user_wallet, name="user-wallet"),
    path("adress-manage/", views.adress_manage, name="adress-manage"),
    path("adress-detail/<int:id>", views.adress_detail, name="adress-detail"),
    path("delete-address/<int:id>", views.adress_delete, name="delete-address"),
    path("order-details/track-order/<int:id>", views.check_detail, name="check-detail"),
    path(
        "order-details/delete-order/<int:id>", views.delete_order, name="delete-order"
    ),
    path("order-details/invoice/<int:id>", views.invoice_order, name="invoice-order"),
    path("change-password/<str:email>", views.change_password, name="change-password"),
]
