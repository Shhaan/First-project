from . import views
from django.urls import path

urlpatterns = [
    # url product
    path('product/',views.product,name='products'),
    path('product/unlist-product/<int:product_id>',views.unlist_product,name='unlist-product'),
    path('product/list-product/<int:product_id>',views.list_product,name='list-product'),
    path('product/<int:product_id>/edit',views.edit_product,name='edit-product'),
    path('product/addproduct/',views.add_product,name='addproduct'),
    path('product/<int:product_id>/edit-image',views.edit_image,name='edit-image'),
    path('product/<int:img_id>/delete-image',views.delete_image,name='delete-image'),
    
    
    
    
    # url brand
    path('brand/',views.brand,name='brand'),
    path('brand/unlist-brand/<int:brand_id>',views.unlist_brand,name='unlist-brand'),
    path('brand/list-brand/<int:brand_id>',views.list_brand,name='list-brand'),
    path('brand/edit-brand/<int:brand_id>',views.edit_brand,name='edit-brand'),
    path('brand/addbrand/',views.add_brand,name='addbrand'),
    
    # url category
    path('category/',views.category,name='category'),
    path('category/unlist-category/<int:category_id>',views.unlist_category,name='unlist-category'),
    path('category/list-category/<int:category_id>',views.list_category,name='list-category'),
    path('category/edit-category/<int:category_id>',views.edit_category,name='edit-category'),
    path('category/addcategory/',views.add_category,name='addcategory'),
    
    
    
   
   
    
]
