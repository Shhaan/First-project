from adminhome.models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import *
from userorder.models import shipping_address


def category(request, category_name):
    if request.user.is_authenticated == False:
        return redirect(reverse("usermain:login"))
    women = request.GET.get("omen", "")
    men = request.GET.get("men", "")
    filter_brand = request.GET.getlist("brand_check")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    price_range_min = int(min_price) if min_price else None
    price_range_max = int(max_price) if max_price else None

    if filter_brand or (price_range_max and price_range_min) or men or women:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(category__Category_name=category_name)
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
            & (
                Q(brand__brand_name__in=filter_brand)
                | (
                    Q(product_price__range=(price_range_min - 1, price_range_max))
                    if price_range_min and price_range_max
                    else Q()
                )
                | (Q(user_gender=women) if women else Q())
                | (Q(user_gender=men) if men else Q())
            )
        )
    else:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(category__Category_name=category_name)
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
        )
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )
    user_cart = Cart.objects.filter(user=request.user)

    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    context = {
        "category": category,
        "brands": brands,
        "products": products,
        "user_cart": user_cart,
        "total": total,
        "category_name": category_name,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }

    return render(request, "productdetail/category.html", context)


def brand(request, brand_name):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")

    women = request.GET.get("Women", "")
    men = request.GET.get("men", "")
    filter_category = request.GET.getlist("category_check")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    price_range_min = int(min_price) if min_price else None
    price_range_max = int(max_price) if max_price else None

    if filter_category or (price_range_max and price_range_min) or men or women:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(brand__brand_name=brand_name)
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
            & (
                Q(category__Category_name__in=filter_category)
                | (
                    Q(product_price__range=(price_range_min - 1, price_range_max))
                    if price_range_min and price_range_max
                    else Q()
                )
                | (Q(user_gender__icontains=women) if women else Q())
                | (Q(user_gender=men) if men else Q())
            )
        )
    else:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(brand__brand_name=brand_name)
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
        )
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    user_cart = Cart.objects.filter(user=request.user)

    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    context = {
        "category": category,
        "brands": brands,
        "products": products,
        "user_cart": user_cart,
        "total": total,
        "brand_name": brand_name,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }
    return render(request, "productdetail/brand.html", context)


def Women(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    filter_category = request.GET.getlist("category_check")
    filter_brand = request.GET.getlist("brand_check")

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    price_range_min = int(min_price) if min_price else None
    price_range_max = int(max_price) if max_price else None

    if filter_category or (price_range_max and price_range_min) or filter_brand:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(user_gender__icontains="women")
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
            & (
                Q(category__Category_name__in=filter_category)
                | Q(brand__brand_name__in=filter_brand)
                | (
                    Q(product_price__range=(price_range_min - 1, price_range_max))
                    if price_range_min and price_range_max
                    else Q()
                )
            )
        )
    else:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(user_gender__icontains="women")
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
        )
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    user_cart = Cart.objects.filter(user=request.user)

    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    context = {
        "category": category,
        "brands": brands,
        "products": products,
        "user_cart": user_cart,
        "total": total,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }
    return render(request, "productdetail/women.html", context)


def men(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    filter_category = request.GET.getlist("category_check")
    filter_brand = request.GET.getlist("brand_check")

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    price_range_min = int(min_price) if min_price else None
    price_range_max = int(max_price) if max_price else None

    if filter_category or (price_range_max and price_range_min) or filter_brand:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(user_gender="MEN")
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
            & (
                Q(category__Category_name__in=filter_category)
                | Q(brand__brand_name__in=filter_brand)
                | (
                    Q(product_price__range=(price_range_min - 1, price_range_max))
                    if price_range_min and price_range_max
                    else Q()
                )
            )
        )
    else:
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(user_gender="MEN")
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
        )
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    user_cart = Cart.objects.filter(user=request.user)

    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    context = {
        "category": category,
        "brands": brands,
        "products": products,
        "user_cart": user_cart,
        "total": total,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }
    return render(request, "productdetail/men.html", context)
