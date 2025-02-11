from django.urls import path
from . import views

urlpatterns = [
    path("category/<str:category_name>", views.category, name="category"),
    path("brand/<str:brand_name>", views.brand, name="brand"),
    path("women/", views.Women, name="women"),
    path("men/", views.men, name="men"),
]
