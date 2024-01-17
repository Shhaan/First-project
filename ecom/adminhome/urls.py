from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("", views.admin_panel, name="admin_panel"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("customer/", views.customer, name="customer"),
    path("customer-block-user/<int:user_id>", views.block_user, name="block-user"),
    path(
        "customer-unblock-user/<int:user_id>", views.unblock_user, name="unblock-user"
    ),
    path("chart-data/", views.get_order_chart_data, name="chart"),
    path("sales-report/", views.sales_report, name="sales-report"),
    path("pdf-download/", views.pdf_downlod, name="pdf_downlod"),
]
