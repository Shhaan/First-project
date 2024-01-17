from adminhome.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Users, Review
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.db.models import *
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from userorder.models import wallet, shipping_address


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect("usermain:home")
    if request.method == "POST":
        email = request.POST["Email-log"]
        password = request.POST["Password-log"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            return redirect("usermain:home")  # Replace with your actual home URL
        else:
            messages.info(request, "Enter a valid user")
            return redirect("usermain:login")

    return render(request, "usermain/Login.html")


def generate_otp():
    return str(random.randint(100000, 999999))


def register(request):
    error = {}
    if request.method == "POST":
        First_name = request.POST["Firstname"]
        Second_name = request.POST["Secondname"]
        Number = request.POST.get("Number")
        Email = request.POST["Email"]
        Gender = request.POST.get("Gender", None)
        Address = request.POST["Address"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        Email_exist = Users.objects.filter(email=Email).exists()

        if password1 != password2:
            error["password_match"] = "Both passwords must be the same"
        elif len(password1) <= 8:
            error["password1"] = "Password must be at least 8 characters"

        if not First_name:
            error["First_name"] = "First name must be entered"

        if Number is None or not Number:
            error["Number"] = "Number must be entered"
        else:
            Number_exist = Users.objects.filter(Number=Number).exists()
            if Number_exist:
                error["Number"] = "Number has been taken"
            elif len(str(Number)) != 10:
                error["Number"] = "Number Must be ten digits"

        if not Email:
            error["Email"] = "Email must be entered"
        elif Email_exist:
            error["Email"] = "Email has been taken"

        if not Address:
            error["Address"] = "Address must be entered"

        if not error:
            user = Users.objects.create_user(
                first_name=First_name,
                last_name=Second_name,
                Number=Number,
                email=Email,
                Gender=Gender,
                Address=Address,
                password=password1,
            )
            wallet.objects.create(user=user, wallet_id=Email + "wallet")
            otp = generate_otp()

            TOTPDevice(user=user, confirmed=True).save()

            user.otp = otp
            user.save()

            subject = "OTP Verification"
            message = f"Your OTP is: {otp}"
            from_email = "shanmohamme.123@gmail.com"
            to_email = [user.email]

            send_mail(subject, message, from_email, to_email)

            user = authenticate(request, email=Email, password=password1)

            if user is not None:
                login(request, user)
                url_success = reverse("usermain:verification")
                return redirect(url_success)

    return render(request, "usermain/Signup.html", {"errors": error})


@login_required
def verification(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp").strip()

        try:
            user = request.user
            if user.otp == entered_otp:
                url = reverse("usermain:home")
                return redirect(url)
            else:
                messages.info(request, "Enter correct otp")
                return redirect(reverse("usermain:verification"))

        except:
            return redirect(reverse("usermain:verification"))

    return render(request, "usermain/Verification.html")


def home(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    else:
        request.session["input_value"] = None
        products = Products.objects.prefetch_related("product_image_set").filter(
            Q(tag__startswith="T")
            & Q(is_deleted=False)
            & Q(brand__is_deleted=False)
            & Q(category__is_deleted=False)
        )[:4]
        category = Category.objects.annotate(num_products=Count("products")).filter(
            Q(num_products__gt=0) & Q(is_deleted=False)
        )

        brands = Brand.objects.annotate(num_products=Count("products")).filter(
            Q(num_products__gt=0) & Q(is_deleted=False)
        )

        user_cart = Cart.objects.filter(user=request.user).order_by("-id")

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
        return render(request, "usermain/Home.html", context)


@login_required
def add_cart(request):
    if request.method == "POST":
        num_product = int(request.POST["num_product"])
        product_name = request.POST["product_name"]
        user = request.user
        product = Products.objects.get(product_name=product_name)
        cart_exist = Cart.objects.filter(user=user, product=product).first()
        if cart_exist:
            if product.quantity >= num_product + cart_exist.quantity:
                Cart.objects.filter(user=user, product=product).update(
                    quantity=F("quantity") + num_product
                )
            else:
                messages.warning(request, "quantity of product is extended")
        else:
            if num_product == 0:
                num_product = 1
            if product.quantity >= num_product:
                Cart.objects.create(user=user, product=product, quantity=num_product)
            else:
                messages.warning(request, "quantity of product is extended")

        return redirect(request.META.get("HTTP_REFERER", "usermain:home"))


@login_required
@require_POST
def update_cart(request):
    try:
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        cart_id = request.POST.get("cart_id")
        product = get_object_or_404(Products, pk=product_id)
        cart_item = get_object_or_404(
            Cart, pk=cart_id, user=request.user, product__pk=product_id
        )

        if quantity > product.quantity:
            response_data = {"qua": product.quantity}
            return JsonResponse(response_data, status=400)

        cart_item.quantity = quantity
        cart_item.save()

        subtotal = quantity * product.product_price
        t = 0
        for i in Cart.objects.filter(user=request.user):
            t += i.quantity * i.product.product_price
        response_data = {"subtotal": subtotal, "quantity": quantity, "total": t}
        return JsonResponse(response_data)

    except Exception as e:
        response_data = {"error": str(e)}
        return JsonResponse(response_data, status=500)


@login_required
def delete_cart(request):
    if request.method == "GET":
        product_id = request.GET.get("product_delete_id")
        if request.user.is_authenticated:
            Cart.objects.get(product__id=product_id, user=request.user).delete()

            return redirect(request.META.get("HTTP_REFERER", "usermain:home"))


@never_cache
def products(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    else:
        request.session["input_value"] = None
        search = request.GET.get("search", "")
        women = request.GET.get("women", "")
        men = request.GET.get("men", "")
        filter_category = request.GET.getlist("category_check")
        filter_brand = request.GET.getlist("brand_check")
        min_price = request.GET.get("min_price", "")
        max_price = request.GET.get("max_price", "")
        price_range_min = int(min_price) if min_price else None
        price_range_max = int(max_price) if max_price else None

        if search:
            products = Products.objects.prefetch_related("product_image_set").filter(
                Q(product_name__icontains=search)
                | Q(category__Category_name__icontains=search)
                | Q(brand__brand_name__icontains=search)
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

            if not brands or not category or not products:
                return redirect(request.META.get("HTTP_REFERER", "usermain:home"))
        elif filter_category or filter_brand:
            products = Products.objects.prefetch_related("product_image_set").filter(
                Q(category__Category_name__in=filter_category)
                | Q(brand__brand_name__in=filter_brand),
                Q(is_deleted=False)
                & Q(brand__is_deleted=False)
                & Q(category__is_deleted=False),
                Q(product_price__range=(price_range_min - 1, price_range_max))
                if price_range_min and price_range_max
                else Q()
                | (Q(user_gender=women) if women else Q())
                | (Q(user_gender=men) if men else Q()),
            )

        else:
            products = Products.objects.prefetch_related("product_image_set").filter(
                Q(is_deleted=False)
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
            "filter_category": filter_category,
            "filter_brand": filter_brand,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        }
    return render(request, "usermain/products.html", context)


@never_cache
def products_detail(request, product_slug):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    product = Products.objects.get(
        Q(slug=product_slug)
        & Q(is_deleted=False)
        & Q(brand__is_deleted=False)
        & Q(category__is_deleted=False)
    )
    user_cart = Cart.objects.filter(user=request.user)
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )
    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )
    related_product = Products.objects.filter(
        (Q(category=product.category) | Q(brand=product.brand))
        & Q(is_deleted=False)
        & Q(brand__is_deleted=False)
        & Q(category__is_deleted=False)
    ).exclude(id=product.id)
    image_product = product_image.objects.select_related("product").filter(
        Q(product=product) & Q(product__is_deleted=False)
    )
    review = Review.objects.select_related("product").filter(
        Q(product__slug=product_slug) & Q(product__is_deleted=False)
    )[:3]
    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price
    request.session["input_value"] = None
    context = {
        "product": product,
        "user_cart": user_cart,
        "category": category,
        "brands": brands,
        "relate": related_product,
        "image_product": image_product,
        "review": review,
        "total": total,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }

    return render(request, "usermain/product-detail.html", context)


def addreview(request, product_slug):
    if request.method == "POST":
        product = Products.objects.get(slug=product_slug)
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        user = request.user
        if not rating or not comment:
            messages.error(
                request, "Please provide all required information for the review."
            )
        else:
            Review.objects.create(
                user=user, product=product, comment=comment, rating=rating
            )
            messages.info(request, "review updated")

    return redirect(request.META.get("HTTP_REFERER"))
