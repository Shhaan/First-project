from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from adminhome.models import *
from usermain.models import Users
from django.db.models import *
from django.views.decorators.cache import never_cache
from userorder.models import *
from django.shortcuts import get_object_or_404


@never_cache
def product(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    search = request.GET.get("search", "")

    if search:
        products = Products.objects.filter(
            Q(product_name__icontains=search)
            | Q(category__Category_name__icontains=search)
            | Q(brand__brand_name__icontains=search)
            | Q(user_gender__icontains=search)
        ).order_by("id")
    else:
        products = Products.objects.all().order_by("id")

    context = {"products": products}

    return render(request, "admincrud/product.html", context)


def unlist_product(request, product_id):
    Products.objects.filter(id=product_id).update(is_deleted=True)
    return redirect(reverse("admincrud:products"))


def list_product(request, product_id):
    Products.objects.filter(id=product_id).update(is_deleted=False)
    return redirect(reverse("admincrud:products"))


@never_cache
def edit_product(request, product_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    errors = {}
    if request.method == "POST":
        product_name = request.POST.get("product_name").strip()
        price = request.POST.get("price")
        gender = request.POST.get("gender")
        post_brand = request.POST.get("brand")
        post_category = request.POST.get("category")
        status = request.POST.get("status")
        quantity = request.POST.get("quantity")
        tag = request.POST.get("tag")
        description = request.POST.get("description").strip()
        exist_product = (
            Products.objects.exclude(id=product_id)
            .filter(product_name=product_name)
            .exists()
        )
        tax_ = request.POST.get("tax")
        if tax_ != "None":
            tax_get = Tax.objects.get(name=tax_)
        else:
            tax_get = None
        if not product_name:
            errors["product_name"] = "Product name can't be None"
        if exist_product:
            errors["exist_product"] = "Product already exists in database"
        if not price:
            errors["price"] = "Price can't be null"
        if not quantity:
            errors["quantity"] = "Quantity can't be null"
        if not description:
            errors["description"] = "Product description must be entered"

        if not errors:
            get_category = Category.objects.get(Category_name=post_category)
            get_brand = Brand.objects.get(brand_name=post_brand)

            Products.objects.filter(id=product_id).update(
                product_name=product_name,
                product_des=description,
                category=get_category,
                brand=get_brand,
                product_price=price,
                user_gender=gender,
                quantity=quantity,
                status=status,
                tag=tag,
                tax_rate=tax_get,
            )
            return redirect(reverse("admincrud:products"))

    product = Products.objects.filter(id=product_id)
    brand = Brand.objects.all()
    category = Category.objects.all()
    tax = Tax.objects.filter(is_deleted=False)
    context = {
        "product": product,
        "brand": brand,
        "category": category,
        "errors": errors,
        "tax": tax,
    }
    return render(request, "admincrud/productedit.html", context)


@never_cache
def add_product(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    errors = {}
    if request.method == "POST":
        product_name = request.POST.get("product_name").strip()
        price = request.POST.get("price")
        gender = request.POST.get("gender")
        brand = request.POST.get("brand")
        category = request.POST.get("category")
        status = request.POST.get("status")
        quantity = request.POST.get("quantity")
        tag = request.POST.get("tag")
        tax_ = request.POST.get("tax")
        if tax_ != "None":
            tax_get = Tax.objects.get(name=tax_)
        else:
            tax_get = None

        description = request.POST.get("description").strip()
        images = request.FILES.getlist("images")

        exist_product = Products.objects.filter(product_name=product_name).first()

        if len(images) > 3:
            errors["imageslen"] = "You can only upload up to 3 images."
        if not images:
            errors["images"] = "Enter atleast one image"
        if exist_product:
            errors["exist_product"] = "Product already exists"
        if not product_name:
            errors["product_name"] = "Product name must be entered"

        if gender == "None":
            errors["gender"] = "Enter user of this Product"
        if not price:
            errors["price"] = "Please enter product price"
        if brand == "None":
            errors["brand"] = "Brand of product must be selected"

        if category == "None":
            errors["category"] = "Category of product must be selected"
        if not quantity:
            errors["quantity"] = "Please enter the available product"
        if not description:
            errors["description"] = "Description of product must be entered"

        if not errors:
            get_category = Category.objects.get(Category_name=category)
            get_brand = Brand.objects.get(brand_name=brand)
            product = Products.objects.create(
                product_name=product_name,
                product_des=description,
                category=get_category,
                brand=get_brand,
                product_price=price,
                user_gender=gender,
                quantity=quantity,
                status=status,
                tag=tag,
                tax_rate=tax_get,
            )

            for file in images:
                product_image.objects.create(product=product, image=file)
            return redirect(reverse("admincrud:products"))
    tax = Tax.objects.filter(is_deleted=False)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {"brands": brands, "categories": categories, "errors": errors, "tax": tax}

    return render(request, "admincrud/productadd.html", context)


def edit_image(request, product_id):
    image_product = product_image.objects.select_related("product").filter(
        product__id=product_id
    )
    product_get = Products.objects.get(id=product_id)
    if request.method == "POST":
        image = request.FILES.get("image")
        if image:
            p_image = product_image(image=image, product=product_get)
            p_image.save()
        for i in image_product:
            image_id = i.id
            image_file = request.FILES.get(f"image_{image_id}")

            if image_file:
                i.image = image_file
                i.save()
        return redirect(reverse("admincrud:products"))

    product = Products.objects.get(id=product_id)
    context = {"image_product": image_product, "product": product}
    return render(request, "admincrud/product-image-edit.html", context)


def delete_image(request, img_id):
    product_image.objects.filter(id=img_id).delete()
    return redirect(request.META.get("HTTP_REFERER"))


@never_cache
def brand(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    search = request.GET.get("search", "")

    if search:
        brand = Brand.objects.filter(Q(brand_name__icontains=search))
    else:
        brand = Brand.objects.all()

    context = {"brand": brand}

    return render(request, "admincrud/brand.html", context)


def unlist_brand(request, brand_id):
    Brand.objects.filter(id=brand_id).update(is_deleted=True)
    return redirect(reverse("admincrud:brand"))


def list_brand(request, brand_id):
    Brand.objects.filter(id=brand_id).update(is_deleted=False)
    return redirect(reverse("admincrud:brand"))


@never_cache
def edit_brand(request, brand_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    errors = {}
    if request.method == "POST":
        image = request.FILES.get("brand_image")

        name = request.POST.get("brand_name").strip()
        exist_brand = Brand.objects.exclude(id=brand_id).filter(brand_name=name).first()

        if exist_brand:
            errors["exist_brand"] = "Brand already exists"
        if not name:
            errors["name"] = "Brand name must be entered"

        if not errors:
            br = Brand.objects.get(id=brand_id)
            if br.brand_name == name and not image:
                return redirect(reverse("admincrud:brand"))
            if image:
                b = Brand.objects.get(id=brand_id)
                b.brand_name = name
                b.brand_image = image
                b.save()
            else:
                b = Brand.objects.get(id=brand_id)
                b.brand_name = name
                b.save()
            return redirect(reverse("admincrud:brand"))

    brand = Brand.objects.get(id=brand_id)

    context = {"brand": brand, "errors": errors}

    return render(request, "admincrud/brandedit.html", context)


@never_cache
def add_brand(request):
    errors = {}
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    if request.method == "POST":
        image = request.FILES.get("brand_image")

        name = request.POST.get("brand_name").strip()
        exist_brand = Brand.objects.filter(brand_name=name).exists()
        if not image:
            errors["image"] = "Enter image of Brand"
        if not name:
            errors["name"] = "Enter name of  Brand"
        if exist_brand:
            errors["exist_brand"] = "Brand already exists"
        if not errors:
            Brand.objects.create(brand_name=name, brand_image=image)
            return redirect(reverse("admincrud:brand"))
    context = {"errors": errors}
    return render(request, "admincrud/brandadd.html", context)


@never_cache
def category(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    search = request.GET.get("search", "")

    if search:
        category = Category.objects.filter(Q(Category_name__icontains=search))
    else:
        category = Category.objects.all()

    context = {"category": category}

    return render(request, "admincrud/category.html", context)


def unlist_category(request, category_id):
    Category.objects.filter(id=category_id).update(is_deleted=True)
    return redirect(reverse("admincrud:category"))


def list_category(request, category_id):
    Category.objects.filter(id=category_id).update(is_deleted=False)
    return redirect(reverse("admincrud:category"))


@never_cache
def edit_category(request, category_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    errors = {}
    if request.method == "POST":
        image = request.FILES.get("category_image")

        name = request.POST.get("category_name").strip()
        exist_category = (
            Category.objects.exclude(id=category_id).filter(Category_name=name).first()
        )

        if exist_category:
            errors["exist_category"] = "Category already exists"
        if not name:
            errors["name"] = "Category name must be entered"

        if not errors:
            ca = Category.objects.get(id=category_id)
            if ca.Category_name == name and not image:
                return redirect(reverse("admincrud:category"))
            if image:
                c = Category.objects.get(id=category_id)
                c.Category_name = name
                c.Category_image = image
                c.save()
            else:
                c = Category.objects.get(id=category_id)
                c.Category_name = name
                c.save()
            return redirect(reverse("admincrud:category"))

    category = Category.objects.get(id=category_id)

    context = {"category": category, "errors": errors}
    return render(request, "admincrud/categoryedit.html", context)


@never_cache
def add_category(request):
    errors = {}
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    if request.method == "POST":
        image = request.FILES.get("category_image")

        name = request.POST.get("category_name").strip()
        exist_category = Category.objects.filter(Category_name=name).exists()
        if not image:
            errors["image"] = "Enter image of category "
        if not name:
            errors["name"] = "Enter name of category "
        if exist_category:
            errors["exist_category"] = "Category already exists"
        if not errors:
            Category.objects.create(Category_name=name, Category_image=image)
            return redirect(reverse("admincrud:category"))
    context = {"errors": errors}
    return render(request, "admincrud/categoryadd.html", context)


def orders(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    search = request.GET.get("search", "")
    if search:
        orderitem = Orderitem.objects.filter(
            (
                Q(id__startswith=search)
                | Q(order__first_name__icontains=search)
                | Q(order__user__email__icontains=search)
                | Q(product__product_name__startswith=search)
                | Q(order__status__icontains=search)
            )
            & ~Q(order__payment_method=None)
        )
    else:
        orderitem = Orderitem.objects.filter(~Q(order__payment_method=None)).order_by(
            "-id"
        )

    return render(request, "admincrud/order.html", {"orderitem": orderitem})


def cancel_order(request, id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    order = Order.objects.get(id=id)
    wallet.objects.filter(user=request.user).update(
        balance=F("balance") + int(round(float(order.total)))
    )
    Order.objects.filter(id=id).update(is_deleted=True)

    return redirect(reverse("admincrud:orders"))


def order_detail(request, id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    orderitem = Orderitem.objects.get(id=id)

    c = CategoryOffer.objects.select_related("category").filter(
        category__Category_name=orderitem.product.category.Category_name
    )
    a = 0
    for i in c:
        a += i.discount_percentage
    return render(
        request,
        "admincrud/order-detail.html",
        {"orderitem": orderitem, "c": a if c else None},
    )


def change_status(request, id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    order = get_object_or_404(Order, id=id)
    current_status = order.status

    STATUS_CHOICES = ["pending", "completed"]

    current_status_index = STATUS_CHOICES.index(current_status)

    next_status_index = (current_status_index + 1) % len(STATUS_CHOICES)
    next_status = STATUS_CHOICES[next_status_index]

    Order.objects.filter(id=id).update(status=next_status)
    return redirect(reverse("admincrud:orders"))


def coupon(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    if request.GET.get("search", ""):
        coupon = Coupon.objects.filter(
            Q(id__startswith=request.GET.get("search", ""))
            | Q(code__icontains=request.GET.get("search", ""))
        )
    else:
        coupon = Coupon.objects.all().order_by("-id")

    return render(request, "admincrud/coupon.html", {"coupon": coupon})


def edit_coupon(request, coupon_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    erorrs = {}
    if request.method == "POST":
        code = request.POST.get("code")
        discount = request.POST.get("discount")
        if not code:
            erorrs["code"] = "Enter code"
        if not discount:
            erorrs["discount"] = "Enter discount_percentage"
        if Coupon.objects.filter(code=code).exclude(id=coupon_id).exists():
            erorrs["code_exits"] = "Enter code already exists"
        if not erorrs:
            Coupon.objects.filter(id=coupon_id).update(
                code=code, discount_percentage=discount
            )

    coupon = Coupon.objects.get(id=coupon_id)

    return render(
        request, "admincrud/coupon-edit.html", {"coupon": coupon, "errors": erorrs}
    )


def add_coupon(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    errors = {}
    if request.method == "POST":
        discount = request.POST.get("discount")
        code = request.POST.get("code")
        if not discount:
            errors["discount"] = "Add discount amount"
        if not code:
            errors["code"] = "Add code for coupon"
        if Coupon.objects.filter(code=code).exists():
            errors["code_exists"] = "Code for coupon exists"
        if not errors:
            Coupon.objects.create(code=code, discount_percentage=discount)
            return redirect("admincrud:coupon")

    return render(request, "admincrud/coupon-add.html", {"errors": errors})


def list_coupon(request, coupon_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    Coupon.objects.filter(id=coupon_id).update(active=True)

    return redirect("admincrud:coupon")


def unlist_coupon(request, coupon_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    Coupon.objects.filter(id=coupon_id).update(active=False)

    return redirect("admincrud:coupon")


def tax(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    if request.GET.get("search", ""):
        tax = Tax.objects.filter(
            Q(id__startswith=request.GET.get("search", ""))
            | Q(name__icontains=request.GET.get("search", ""))
        )
    else:
        tax = Tax.objects.all().order_by("-id")

    return render(request, "admincrud/tax.html", {"tax": tax})


def edit_tax(request, tax_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    erorrs = {}
    if request.method == "POST":
        name = request.POST.get("name")
        percentage = request.POST.get("percentage")
        if not name:
            erorrs["name"] = "Enter name of tax"
        if not percentage:
            erorrs["percentage"] = "Enter percentage"
        if Tax.objects.filter(name__icontains=name).exclude(id=tax_id).exists():
            erorrs["tax_exits"] = "Enter Tax already exists"
        if not erorrs:
            Tax.objects.filter(id=tax_id).update(name=name, rate=percentage)

    tax = Tax.objects.get(id=tax_id)

    return render(request, "admincrud/tax-edit.html", {"tax": tax, "errors": erorrs})


def add_tax(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    errors = {}
    if request.method == "POST":
        percentage = request.POST.get("percentage")
        name = request.POST.get("name")
        if not percentage:
            errors["percentage"] = "Add percentage amount"
        if not name:
            errors["name"] = "Add name for Tax"
        if Tax.objects.filter(name=name).exists():
            errors["name_exists"] = "Name for tax exists"
        if not errors:
            Tax.objects.create(name=name, rate=percentage)
            return redirect("admincrud:tax")

    return render(request, "admincrud/tax-add.html", {"errors": errors})


def list_tax(request, tax_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    Tax.objects.filter(id=tax_id).update(is_deleted=False)

    return redirect("admincrud:tax")


def unlist_tax(request, tax_id):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    Tax.objects.filter(id=tax_id).update(is_deleted=True)

    return redirect("admincrud:tax")
