from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from adminhome.models import *
from usermain.models import Users
from django.db.models import *
from django.views.decorators.cache import never_cache

# Create your views here.


# view for products
@never_cache
def product(request):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')   
    
    search = request.GET.get('search','')
    
    if search:
        products = Products.objects.filter(Q(product_name__icontains=search) | Q(category__Category_name__icontains=search) | Q(brand__brand_name__icontains=search)| Q(user_gender__icontains = search)).order_by('id')
    else:
        
        products = Products.objects.all().order_by('id')
    
    context = {'products':products}
    
    return render(request,'admincrud/product.html',context)
def unlist_product(request,product_id):
    Products.objects.filter(id = product_id).update(is_deleted=True)
    return redirect(reverse('admincrud:products'))
def list_product(request,product_id):
    Products.objects.filter(id = product_id).update(is_deleted=False)
    return redirect(reverse('admincrud:products'))
@never_cache
def edit_product(request,product_id):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    errors = {}
    if request.method =='POST':
        
        product_name = request.POST.get('product_name').strip()
        price = request.POST.get('price')
        gender = request.POST.get('gender')
        post_brand = request.POST.get('brand')
        post_category = request.POST.get('category')
        status = request.POST.get('status')
        quantity = request.POST.get('quantity')
        tag = request.POST.get('tag') 
        description = request.POST.get('description').strip()
        exist_product = Products.objects.exclude(id=product_id).filter(product_name = product_name).exists()
 
        if not product_name:
            errors['product_name'] = "Product name can't be None"
        if  exist_product :
            errors['exist_product'] = 'Product already exists in database'
        if not price:
            errors['price'] = "Price can't be null"
        if not quantity:
            errors['quantity'] = "Quantity can't be null"
        if not description:
            errors['description'] = "Product description must be entered" 
            
        if not errors:
            get_category = Category.objects.get(Category_name = post_category)
            get_brand = Brand.objects.get(brand_name = post_brand)
            
            Products.objects.filter(id = product_id).update(product_name=product_name,product_des = description,category = get_category,brand =get_brand,product_price = price,user_gender =gender,quantity = quantity,status= status,tag=tag)
            return redirect(reverse('admincrud:products'))
                 
    product = Products.objects.filter(id = product_id)
    brand = Brand.objects.all()
    category = Category.objects.all()
    context = {'product':product,'brand':brand,'category':category,'errors':errors,}
    return render(request,'admincrud/productedit.html',context)
@never_cache
def add_product(request):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    errors = {}
    if request.method == 'POST':
        product_name = request.POST.get('product_name').strip()
        price = request.POST.get('price')
        gender = request.POST.get('gender')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        status = request.POST.get('status')
        quantity = request.POST.get('quantity')
        tag = request.POST.get('tag')
        description = request.POST.get('description').strip()
        images = request.FILES.getlist('images')
        exist_product = Products.objects.filter(product_name=product_name).first()
      
        if len(images) > 3:
            errors['imageslen'] = "You can only upload up to 3 images."
        if not images:
            errors['images'] = 'Enter atleast one image'
        if  exist_product :
            errors['exist_product'] = 'Product already exists'
        if not product_name :
            errors['product_name'] = 'Product name must be entered'

        if  gender == 'None':
            errors['gender'] = 'Enter user of this Product'
        if not price:
            errors['price'] = 'Please enter product price'
        if brand == 'None':
            errors['brand'] = 'Brand of product must be selected'
        if category == 'None':
            errors['category'] = 'Category of product must be selected'
        if not quantity:
            errors['quantity'] = 'Please enter the available product'
        if not description:
            errors['description'] = 'Description of product must be entered'
            
        
            
        if not errors:
            get_category = Category.objects.get(Category_name = category)
            get_brand = Brand.objects.get(brand_name = brand)
            product = Products.objects.create(product_name=product_name,product_des = description,category = get_category,brand =get_brand,product_price = price,user_gender =gender,quantity = quantity,status= status,tag=tag)
            
          
            for file in images:
                product_image.objects.create(product=product, image=file)
            return redirect(reverse('admincrud:products'))
            
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {'brands': brands, 'categories': categories, 'errors': errors}

    return render(request, 'admincrud/productadd.html', context)
 
def edit_image(request,product_id):
    image_product = product_image.objects.select_related('product').filter(product__id = product_id)
    product_get = Products.objects.get(id = product_id)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            p_image = product_image(image = image,product = product_get)
            p_image.save()
        for i in image_product:
            image_id = i.id
            image_file = request.FILES.get(f'image_{image_id}')
            
            if image_file:
                i.image = image_file
                i.save()
        return redirect(reverse('admincrud:products'))

             
         
    product = Products.objects.get(id = product_id)
    context = {'image_product':image_product,'product':product}
    return  render(request,'admincrud/product-image-edit.html',context)
def delete_image(request,img_id):
    product_image.objects.filter(id = img_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))
    
# view for Brand
@never_cache
def brand(request):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')   
    
    search = request.GET.get('search','')
    
    if search:
        brand = Brand.objects.filter(Q(brand_name__icontains=search))
    else:
        
        brand = Brand.objects.all()
    
    
    context = {'brand':brand}
    
    return render(request,'admincrud/brand.html',context)
def unlist_brand(request,brand_id):
    Brand.objects.filter(id = brand_id).update(is_deleted=True)
    return redirect(reverse('admincrud:brand'))

def list_brand(request,brand_id):
    Brand.objects.filter(id = brand_id).update(is_deleted=False)
    return redirect(reverse('admincrud:brand'))
@never_cache
def edit_brand(request,brand_id):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    errors = {}
    if request.method == 'POST':
        image = request.FILES.get('brand_image')
        
        name = request.POST.get('brand_name').strip()
        exist_brand = Brand.objects.exclude(id=brand_id).filter(brand_name = name).first()
        
        if  exist_brand :
            errors['exist_brand'] = 'Brand already exists'
        if not name :
            errors['name'] = 'Brand name must be entered'
        
        
        if not errors:
            br = Brand.objects.get(id = brand_id)
            if br.brand_name == name  and not image:
                
                return redirect(reverse('admincrud:brand'))
            if image:
                
                b =  Brand.objects.get(id=brand_id)
                b.brand_name = name
                b.brand_image = image
                b.save()
            else:
                
                b =  Brand.objects.get(id=brand_id)
                b.brand_name = name
                b.save()
            return redirect(reverse('admincrud:brand'))
        
    brand = Brand.objects.get(id = brand_id)
    
    context = {'brand':brand,'errors':errors}
    
    
    return render(request,'admincrud/brandedit.html',context)

@never_cache
def add_brand(request):
    errors = {}
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    
    if request.method == 'POST':
        
        image = request.FILES.get('brand_image')
        
        name = request.POST.get('brand_name').strip()
        exist_brand = Brand.objects.filter(brand_name = name).exists()
        if not image:
            errors['image'] ='Enter image of Brand'
        if not name:
            errors['name'] ='Enter name of  Brand'
        if  exist_brand:
            errors['exist_brand'] ='Brand already exists'
        if not errors:
            Brand.objects.create(brand_name=name,brand_image = image)
            return redirect(reverse('admincrud:brand'))
    context = {'errors':errors}
    return render(request,'admincrud/brandadd.html',context)
# view for category

@never_cache
def category(request):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')   
    search = request.GET.get('search','')
    
    if search:
        category = Category.objects.filter(Q(Category_name__icontains=search) )
    else:
        
        category = Category.objects.all()
    
    
    
    context = {'category':category}
    
    return render(request,'admincrud/category.html',context)
def unlist_category(request,category_id):
    Category.objects.filter(id = category_id).update(is_deleted=True)
    return redirect(reverse('admincrud:category'))

def list_category(request,category_id):
    Category.objects.filter(id = category_id).update(is_deleted=False)
    return redirect(reverse('admincrud:category'))
@never_cache
def edit_category(request,category_id):
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    
    errors = {}
    if request.method == 'POST':
        image = request.FILES.get('category_image')
        
        name = request.POST.get('category_name').strip()
        exist_category = Category.objects.exclude(id=category_id).filter(Category_name = name).first()
        
        if  exist_category :
            errors['exist_category'] = 'Category already exists'
        if not name :
            errors['name'] = 'Category name must be entered'
        
        
        if not errors:
            ca = Category.objects.get(id = category_id)
            if ca.Category_name == name  and not image:
                
                return redirect(reverse('admincrud:category'))
            if image:
                c =  Category.objects.get(id=category_id)
                c.Category_name = name
                c.Category_image = image
                c.save()
            else:
                c =  Category.objects.get(id=category_id)
                c.Category_name = name
                c.save()
            return redirect(reverse('admincrud:category'))
        
    category = Category.objects.get(id = category_id)
    
    context = {'category':category,'errors':errors}
    return render(request,'admincrud/categoryedit.html',context)

@never_cache
def add_category(request):
    errors = {}
    if   request.user.is_superuser == False:
        return redirect('adminhome:admin_login')  
    
    if request.method == 'POST':
        
        image = request.FILES.get('category_image')
        
        name = request.POST.get('category_name').strip()
        exist_category = Category.objects.filter(Category_name = name).exists()
        if not image:
            errors['image'] ='Enter image of category '
        if not name:
            errors['name'] ='Enter name of category '
        if  exist_category:
            errors['exist_category'] ='Category already exists'
        if not errors:
            Category.objects.create(Category_name=name,Category_image = image)
            return redirect(reverse('admincrud:category'))
    context = {'errors':errors}
    return render(request,'admincrud/categoryadd.html',context)