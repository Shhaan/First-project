from django.shortcuts import render
from adminhome.models import *
from django.shortcuts import render, redirect
from django.urls import reverse
from usermain.models import Users
from django.contrib import messages

from django.db.models import *
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from userorder.models import *
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .forms import *
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.
def profile(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")

    total = 0

    for cart_item in user_cart:
        total += cart_item.quantity * cart_item.product.product_price

    user = request.user

    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    context = {
        "user_cart": user_cart,
        "total": total,
        "user": user,
        "category": category,
        "brands": brands,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }
    return render(request, "userprofile/profile.html", context)


def user_logout(request):
    logout(request)

    return redirect("usermain:login")


def profile_edit(request, id):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    errors = {}
    if request.method == "POST":
        f_name = request.POST.get("first_name").strip()
        l_name = request.POST["last_name"]
        gender = request.POST["gender"]
        number = request.POST["number"]
        email = request.POST["email"]
        address = request.POST.get("address").strip()
        email_exist = Users.objects.exclude(id=id).filter(email=email).exists()
        number_exist = Users.objects.exclude(id=id).filter(Number=number).exists()
        if not f_name:
            errors["f_name"] = "Enter First name"
        if not number:
            errors["number"] = "Enter Number"
        if not address:
            errors["address"] = "Enter Address"
        if not email:
            errors["email"] = "Enter email"
        if email_exist:
            errors["email_exist"] = "Email already taken"
        if number_exist:
            errors["number_exist"] = "Number already taken"
        if not errors:
            Users.objects.filter(id=id).update(
                first_name=f_name,
                last_name=l_name,
                Number=number,
                Address=address,
                email=email,
                Gender=gender,
            )
            return redirect(request.META.get("HTTP_REFERER"))

    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    total = 0

    for i in user_cart:
        total += i.quantity * i.product.product_price

    user = request.user
    context = {
        "user_cart": user_cart,
        "total": total,
        "errors": errors,
        "category": category,
        "brands": brands,
        "shipping_adress": shipping_address.objects.filter(user=request.user),
    }

    return render(request, "userprofile/profile-edit.html", context)


def user_order(request):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    order_item = Orderitem.objects.filter(
        ~Q(order__payment_method=None) & Q(order__user=request.user)
    )
    order = (
        Order.objects.annotate(num=Count("order_items"))
        .filter(
            ~Q(payment_method=None)
            & Q(user=request.user)
            & Q(num__gt=0)
            & Q(is_deleted=False)
        )
        .order_by("id")
    )

    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    return render(
        request,
        "userprofile/user-order.html",
        {
            "order_item": order_item,
            "order": order,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


def check_detail(request, id):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    order = Order.objects.prefetch_related("order_items").get(id=id)
    return render(
        request,
        "userprofile/order-detail-user.html",
        {
            "order": order,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


def delete_order(request, id):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    order = Order.objects.get(id=id)
    wallet.objects.filter(user=request.user).update(
        balance=F("balance") + int(round(float(order.total)))
    )
    Order.objects.filter(id=id).update(is_deleted=True)

    return redirect("userprofile:user-order")


@login_required(login_url="usermain:login")
def invoice_order(request, id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    header = Paragraph("<b>Invoice</b>", styles["Heading1"])
    elements.append(header)

    elements.append(Spacer(1, 12))

    data_labels = [
        "Order Number",
        "First Name",
        "Email",
        "Number",
        "Product Name",
        "Ordered Date",
        "Product Tax",
        "Shipping price",
        "Coupon",
        "Quantity",
        "Subtotal",
        "Category offer",
        "Item Total",
        "Order Total",
        "Paid amount",
    ]

    orders = Orderitem.objects.select_related("order").filter(Q(order__id=id))

    data_values = [data_labels]

    for i in orders:
        user = i.order.user
        product = i.product

        tax_rate = product.tax_rate.rate if product.tax_rate else None
        coupon = i.order.coupon.discount_percentage if i.order.coupon else None
        c = CategoryOffer.objects.filter(
            category=Category.objects.get(
                Category_name=i.product.category.Category_name
            )
        )
        a = 0
        for z in c:
            a += z.discount_percentage
        row_data = [
            i.pk,
            user.first_name,
            user.email,
            user.Number,
            product.product_name,
            i.order.created_at.strftime("%Y-%m-%d"),
            float(tax_rate) if tax_rate else 0,
            i.shipping_option.shipping_price,
            coupon if coupon else 0,
            i.quantity,
            i.sub_total,
            a,
            i.total,
            i.order.total,
            i.order.paid_amount,
        ]

        data_values.append(row_data)

    for i in range(len(orders)):
        elements.append(Paragraph(f"Order item {i+1}", styles["Heading2"]))
        invoice_details = [
            Paragraph(
                f"<b>{label}:</b> {value}<br/><br/>"
                if value
                else f"<b>{label}:</b><br/><br/>",
                styles["Normal"],
            )
            for label, value in zip(data_values[0], data_values[i + 1])
        ]
        elements.extend(invoice_details)

        elements.append(Spacer(1, 12))

    footer = Paragraph("<i>Thank you for your purchase!</i>", styles["Normal"])
    elements.append(footer)

    doc.build(elements)
    return response


@login_required(login_url="usermain:login")
def change_password(request, email):
    error = {}
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            error["incorect"] = "Incorrect current password."

        if len(new_password) <= 8:
            error["len"] = "Password must be eight letter."
        if new_password != confirm_password:
            error["confirm"] = "New password and confirm password do not match."

        if not error:
            request.user.set_password(new_password)
            request.user.save()
            return redirect(reverse("usermain:login"))
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    return render(
        request,
        "userprofile/change-password.html",
        {
            "errors": error,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


@login_required(login_url="usermain:login")
def user_wallet(request):
    if wallet.objects.filter(user=request.user).exists():
        wallet_user = wallet.objects.get(user=request.user)
    else:
        wallet_user = wallet.objects.create(
            user=request.user, wallet_id=request.user.email + "wallet"
        )
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    return render(
        request,
        "userprofile/wallet.html",
        {
            "wallet": wallet_user,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


@login_required(login_url="usermain:login")
def adress_manage(request):
    if request.method == "POST":
        form = Shipping_adress_Form(request.POST)
        if form.is_valid():
            shipping_addres = form.save(commit=False)
            shipping_addres.user = request.user
            shipping_addres.save()
            return redirect("userprofile:adress-manage")
    else:
        form = Shipping_adress_Form()
    address_shipping = shipping_address.objects.filter(user=request.user)
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )
    return render(
        request,
        "userprofile/shipping-adress.html",
        {
            "address_shipping": address_shipping,
            "form": form,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


@login_required(login_url="usermain:login")
def adress_detail(request, id):
    if request.method == "POST":
        address = request.POST.get("address")
        first_name = request.POST.get("first_name")
        second_name = request.POST.get("second_name")

        postal_code = request.POST.get("postal_code")
        phone = request.POST.get("phone")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")

        if address and postal_code and phone and district and state and country:
            shipping_address.objects.filter(id=id).update(
                address=address,
                postal_code=postal_code,
                phone=phone,
                district=district,
                state=state,
                country=country,
                second_name=second_name,
                first_name=first_name,
            )
            return redirect(reverse("userprofile:adress-manage"))
        else:
            messages.info(request, "Fill all the field")
    adress_shipping = shipping_address.objects.get(id=id)
    user_cart = Cart.objects.filter(user=request.user).order_by("-id")
    category = Category.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )

    brands = Brand.objects.annotate(num_products=Count("products")).filter(
        Q(num_products__gt=0) & Q(is_deleted=False)
    )
    return render(
        request,
        "userprofile/address-detail.html",
        {
            "adress_shipping": adress_shipping,
            "user_cart": user_cart,
            "category": category,
            "brands": brands,
            "shipping_adress": shipping_address.objects.filter(user=request.user),
        },
    )


@login_required(login_url="usermain:login")
def adress_delete(request, id):
    shipping_address.objects.filter(id=id).delete()

    return redirect(reverse("userprofile:adress-manage"))
