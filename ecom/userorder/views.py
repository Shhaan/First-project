from django.shortcuts import render
from adminhome.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import (
    Order,
    Orderitem,
    shipping,
    Coupon,
    shipping_address,
    CategoryOffer,
    wallet,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from django.db.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm


@never_cache
def chekout_pr_in(request, slug):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    request.session["input_value"] = None
    if request.method == "POST":
        input_val = request.POST["value"]

        p = Products.objects.get(slug=slug)

        if int(input_val) > int(p.quantity):
            messages.warning(request, f"there are only {p.quantity} left")
            return redirect(
                reverse("usermain:products-detail", kwargs={"product_slug": slug})
            )
        request.session["input_value"] = input_val.strip()

        if shipping_address.objects.filter(user=request.user).exists():
            return redirect(
                reverse(
                    "userorder:checkout-with-shipping-adderss", kwargs={"slug": slug}
                )
            )
        else:
            return redirect(reverse("userorder:checkout", kwargs={"slug": slug}))


login_required(login_url="usermain:login")


def checkout_shipping_address(request, slug):
    product = Products.objects.get(slug=slug)

    error = {}
    if request.method == "POST":
        shipping_addsd = request.POST.get("shipping_add")

        if not shipping_addsd:
            error["shipping_add"] = "Please select any of above"
        print(shipping_addsd)
        if not error:
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address.objects.get(id=shipping_addsd),
            )

            user_cart = Cart.objects.filter(user=request.user, product=product)

            quantity = 0
            for i in user_cart:
                total = i.product.product_price * i.quantity
                quantity = i.quantity

            input_val = request.session.get("input_value", "")

            if input_val:
                total = int(input_val) * product.product_price
                o_t = Orderitem.objects.create(
                    order=order, product=product, quantity=input_val, sub_total=total
                )
                request.session["cart_true"] = False
            else:
                o_t = Orderitem.objects.create(
                    order=order, product=product, quantity=quantity, sub_total=total
                )
                request.session["cart_true"] = True
                request.session["pr_slug"] = slug

            return redirect(
                reverse(
                    "userorder:shipping",
                    kwargs={"slug": slug, "ot": o_t.slug, "o": order.slug},
                )
            )
    ship = shipping.objects.all()
    total_context = 0
    input_val = request.session.get("input_value", "")
    if input_val:
        total_context = int(input_val) * product.product_price
    else:
        user_cart = Cart.objects.filter(user=request.user, product=product)

        quantity = 0
        for i in user_cart:
            total_context = i.product.product_price * i.quantity
    tax = 0
    if product.tax_rate:
        tax = total_context * product.tax_rate.rate / 100
    category_offer_var = CategoryOffer.objects.select_related("category").filter(
        category__Category_name=product.category.Category_name
    )
    d = 0
    if category_offer_var:
        for i in category_offer_var:
            d += i.discount_percentage
    total_context -= d
    total_context += tax
    context = {
        "product": product,
        "errors": error,
        "ship": ship,
        "total_context": total_context,
        "subtotal": total_context + d - tax,
        "d": d if d != 0 else None,
        "shippping_address": shipping_address.objects.filter(user=request.user)[:4],
    }

    return render(request, "userorder/checkout-with-address.html", context)


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def checkout(request, slug):
    if request.user.is_authenticated == False:
        return redirect("usermain:login")
    error = {}

    product = Products.objects.get(slug=slug)

    if request.method == "POST":
        f_name = request.POST.get("f_name").strip()
        l_name = request.POST.get("l_name").strip()
        phone = request.POST["phone"]
        Address = request.POST.get("Address").strip()
        country = request.POST.get("country").strip()
        district = request.POST.get("district").strip()

        state = request.POST.get("state").strip()
        postalcode = request.POST.get("postalcode").strip()

        user = request.user

        if not f_name:
            error["First_name"] = "First name must be entered"
        if not l_name:
            error["last_name"] = "Last name must be entered"

        if not phone:
            error["Number"] = "Number must be entered"

        if not country:
            error["country"] = "country must be entered"
        if not state:
            error["state"] = "state must be entered"
        if not postalcode:
            error["postalcode"] = "postalcode must be entered"

        if not Address:
            error["Address"] = "Address must be entered"
        if not district:
            error["district"] = "Enter district"

        if not error:
            sh = shipping_address.objects.create(
                user=request.user,
                first_name=f_name,
                second_name=l_name,
                postal_code=postalcode,
                address=Address,
                district=district,
                country=country,
                state=state,
                phone=phone,
            )

            order = Order.objects.create(
                user=user, shipping_address=sh, first_name=request.user.first_name
            )

            user_cart = Cart.objects.filter(user=request.user, product=product)

            quantity = 0
            for i in user_cart:
                total = i.product.product_price * i.quantity
                quantity = i.quantity

            input_val = request.session.get("input_value", "")

            if input_val:
                total = int(input_val) * product.product_price
                o_t = Orderitem.objects.create(
                    order=order, product=product, quantity=input_val, sub_total=total
                )
                request.session["cart_true"] = False

            else:
                o_t = Orderitem.objects.create(
                    order=order, product=product, quantity=quantity, sub_total=total
                )
                request.session["cart_true"] = True
                request.session["pr_slug"] = slug

            return redirect(
                reverse(
                    "userorder:shipping",
                    kwargs={"slug": slug, "ot": o_t.slug, "o": order.slug},
                )
            )

    ship = shipping.objects.all()
    total_context = 0
    input_val = request.session.get("input_value", "")
    if input_val:
        total_context = int(input_val) * product.product_price
    else:
        user_cart = Cart.objects.filter(user=request.user, product=product)

        quantity = 0
        for i in user_cart:
            total_context = i.product.product_price * i.quantity

    tax = 0
    if product.tax_rate:
        tax = total_context * product.tax_rate.rate / 100
    category_offer_var = CategoryOffer.objects.select_related("category").filter(
        category__Category_name=product.category.Category_name
    )
    d = 0
    if category_offer_var:
        for i in category_offer_var:
            d += i.discount_percentage
    total_context -= d
    total_context += tax

    context = {
        "product": product,
        "errors": error,
        "ship": ship,
        "total_context": total_context,
        "subtotal": total_context + d - tax,
        "d": d if d != 0 else None,
    }
    return render(request, "userorder/checkout.html", context)


@never_cache
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url="usermain:login")
def shippin(request, slug, o, ot):
    product = Products.objects.get(slug=slug)
    order_id = ot

    order = Orderitem.objects.get(slug=order_id)
    ship = shipping.objects.all()
    total = (
        order.sub_total
        if product.tax_rate is None
        else order.sub_total + order.sub_total * (product.tax_rate.rate / 100)
    )
    category_offer_var = CategoryOffer.objects.select_related("category").filter(
        category__Category_name=product.category.Category_name
    )
    category_discount = 0
    for i in category_offer_var:
        category_discount += i.discount_percentage

    if category_offer_var:
        total -= category_discount
    context = {
        "product": product,
        "ship": ship,
        "order": order,
        "o_slug": o,
        "ot_slug": ot,
        "order_item": total,
        "d": category_discount if category_discount != 0 else None,
    }
    return render(request, "userorder/shipping.html", context)


@login_required(login_url="usermain:login")
def shippin_add(request, slug, o, ot):
    if request.method == "POST":
        request.session["input_value"] = None
        shipp = request.POST.get("shipping")
        obj = shipping.objects.get(shipping_name=shipp)
        Orderitem.objects.filter(slug=ot).update(shipping_option=obj)
    return redirect(
        reverse("userorder:payment-detail", kwargs={"slug": slug, "o": o, "ot": ot})
    )


# def update_total(request,ot):
#     if request.method == "POST":
#         data = json.loads(request.body.decode('utf-8'))

#         sub_total = int(data.get('subTotal', 0))
#         shipping_price = int(data.get('shippingPrice', 0))
#         tax_rate = int(data.get('taxRate', 0))
#         coupon = int(data.get('coupon', 0))
#         if coupon == 0:
#             total = (sub_total + shipping_price + ( tax_rate * sub_total /100) )
#         else:
#             discount_amount = (sub_total + shipping_price) * (coupon / 100)
#             total = sub_total + shipping_price - discount_amount
#         Orderitem.objects.filter(slug = ot).update(total = total)
#         return JsonResponse({'total': total})


def payment_detail(request, slug, o, ot):
    product = Products.objects.get(slug=slug)
    order_item_slug = ot

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = json.loads(request.body.decode("utf-8"))

        category_offer_var = CategoryOffer.objects.select_related("category").filter(
            category__Category_name=product.category.Category_name
        )
        c = 0
        if category_offer_var:
            for i in category_offer_var:
                c += i.discount_percentage

        sub_total = int(data.get("subTotal", 0))
        shipping_price = int(data.get("shippingPrice", 0))
        tax_rate = float(data.get("taxRate", 0))
        coupon = int(data.get("coupon", 0))
        if coupon == 0 or coupon == None:
            total = float(sub_total + shipping_price + (tax_rate * sub_total / 100))
        else:
            coupon_discount = float((sub_total + shipping_price) * (coupon / 100))
            tax_amount = float(tax_rate * (sub_total + shipping_price) / 100)
            coupeon_tot = float(sub_total - coupon_discount)
            total = round(float(coupeon_tot + shipping_price - tax_amount), 2)
        total -= float(c)
        Orderitem.objects.filter(slug=ot).update(total=total)
        return JsonResponse({"total": total})

    order = Orderitem.objects.get(slug=order_item_slug)
    coupen_order = Order.objects.filter(Q(slug=o) & ~Q(coupon=None))

    pay_tax = Decimal(0)
    session_coupon = 0
    for i in coupen_order:
        session_coupon += float(i.coupon.discount_percentage)
    if order.product.tax_rate:
        pay_tax = order.product.tax_rate.rate

    if not coupen_order or coupen_order == None:
        pay_total = float(
            order.sub_total
            + order.shipping_option.shipping_price
            + (pay_tax * order.sub_total / 100)
        )

    else:
        coupon_discount = float(
            (order.sub_total + order.shipping_option.shipping_price)
            * (session_coupon / 100)
        )
        tax_amount = float(
            pay_tax * (order.sub_total + order.shipping_option.shipping_price) / 100
        )
        pay_total_coupen = order.sub_total - coupon_discount
        pay_total = float(
            pay_total_coupen + order.shipping_option.shipping_price - tax_amount
        )

    category_offer_var = CategoryOffer.objects.select_related("category").filter(
        category__Category_name=product.category.Category_name
    )
    c = 0
    if category_offer_var:
        for i in category_offer_var:
            c += i.discount_percentage
    pay_total -= float(c)

    request.session["total"] = pay_total

    if request.method == "POST":
        payment = request.POST.get("payment")

        if not payment:
            messages.info(request, "Please select any of above")
            return redirect(
                reverse(
                    "userorder:payment-detail", kwargs={"slug": slug, "o": o, "ot": ot}
                )
            )
        else:
            if payment == "pay_by_wallet":
                w = wallet.objects.get(user=request.user)

                if float(w.balance) < pay_total:
                    messages.info(request, "Wallet money is not enough")
                    return redirect(
                        reverse(
                            "userorder:payment-detail",
                            kwargs={"slug": slug, "o": o, "ot": ot},
                        )
                    )
                else:
                    Order.objects.filter(slug=o).update(
                        payment_method=payment,
                        paid=True,
                        paid_amount=round(pay_total, 2),
                    )
                    w.balance -= pay_total
                    w.save()

                    request.session["order_slug"] = None
                    return redirect(reverse("userorder:payment-success"))

            if payment == "cash_on_delivery":
                Order.objects.filter(slug=o).update(
                    payment_method=payment, paid=False, paid_amount=0
                )
                request.session["order_slug"] = None
                return redirect(reverse("userorder:payment-success"))

    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": pay_total,
        "item_name": product.product_name,
        "invoice": str(order.pk),
        "currency_code": "USD",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('userorder:payment-success')}",
        "cancel_url": f"http://{host}{reverse('userorder:payment-failed')}",
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    Order.objects.filter(slug=o).update(total=pay_total)

    request.session["order_slug"] = o
    request.session["order_id"] = Order.objects.get(slug=o).pk
    context = {
        "product": product,
        "order": order,
        "coupon": session_coupon,
        "form": form,
        "o_slug": o,
        "ot_slug": ot,
        "order_coupon": Order.objects.get(slug=o),
        "c": c if c != 0 else None,
    }
    return render(request, "userorder/payment.html", context)


def apply_coupon(request, o, ot, slug):
    if request.method == "POST":
        coupon = request.POST["c"].strip()
        slug = request.POST["slug"]
        if coupon:
            coupon_obj = Coupon.objects.filter(Q(code=coupon) & Q(active=True)).first()
            if coupon_obj:
                Order.objects.filter(slug=o).update(
                    coupon=Coupon.objects.get(code=coupon)
                )
            else:
                messages.error(request, "Coupon has expired")

    return redirect(
        reverse("userorder:payment-detail", kwargs={"slug": slug, "o": o, "ot": ot})
    )


@login_required(login_url="usermain:login")
def bulk_buy_address(request):
    error = {}
    cart_item = Cart.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    ship = shipping.objects.all()

    t = 0
    category_price_disc = 0

    for item in cart_item:
        t += item.product.product_price * item.quantity

        if item.product.tax_rate:
            total_tax = t * item.product.tax_rate.rate / 100
            t += total_tax
        category_offer_var = CategoryOffer.objects.select_related("category").filter(
            category__Category_name=item.product.category.Category_name
        )

        if category_offer_var:
            for offer in category_offer_var:
                category_price_disc += offer.discount_percentage

    t -= category_price_disc

    if request.method == "POST":
        shipping_add_id = request.POST.get("shipping_add")
        shipping_name = request.POST.get("ship")

        if not shipping_add_id:
            error["shipping_add_id"] = "Please select any of above"

        if not error:
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address.objects.get(id=int(shipping_add_id)),
                first_name=request.user.first_name,
            )
            all_total = 0
            for item in cart_item:
                t = 0
                total_tax = 0
                t += item.product.product_price * item.quantity

                if item.product.tax_rate:
                    total_tax = (t * item.product.tax_rate.rate) / 100
                    t += total_tax

                category_offer_var = CategoryOffer.objects.select_related(
                    "category"
                ).filter(category__Category_name=item.product.category.Category_name)

                if category_offer_var:
                    category_price_disc = 0

                    for i in category_offer_var:
                        category_price_disc += i.discount_percentage
                t -= category_price_disc
                all_total += t
                o = Orderitem.objects.create(
                    product=item.product,
                    shipping_option=shipping.objects.get(shipping_name=shipping_name),
                    order=order,
                    sub_total=item.product.product_price * item.quantity,
                    quantity=item.quantity,
                    total=t,
                )
            Order.objects.filter(id=order.pk).update(total=all_total)
            return redirect(
                reverse(
                    "userorder:bulk-buy-payment",
                    kwargs={"order_slug": order.slug, "o": o.slug},
                )
            )

    context = {
        "ship": ship,
        "t": round(t, 2),
        "errors": error,
        "cart_item": cart_item,
        "shippping_address": shipping_address.objects.filter(user=request.user)[:4],
        "c": category_price_disc if category_price_disc != 0 else None,
    }
    return render(request, "userorder/checkout-bulk-address.html", context)


@login_required(login_url="usermain:login")
def bulk_buy(request):
    error = {}
    cart_item = Cart.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    ship = shipping.objects.all()

    t = 0
    category_price_disc = 0

    for item in cart_item:
        t += item.product.product_price * item.quantity

        if item.product.tax_rate:
            total_tax = t * item.product.tax_rate.rate / 100
            t += total_tax
        category_offer_var = CategoryOffer.objects.select_related("category").filter(
            category__Category_name=item.product.category.Category_name
        )

        if category_offer_var:
            for offer in category_offer_var:
                category_price_disc += offer.discount_percentage

    t -= category_price_disc
    if request.method == "POST":
        f_name = request.POST.get("f_name").strip()
        l_name = request.POST.get("l_name").strip()
        phone = request.POST["phone"]
        Address = request.POST.get("Address").strip()
        country = request.POST.get("country").strip()
        state = request.POST.get("state").strip()
        postalcode = request.POST.get("postalcode").strip()
        shipping_name = request.POST.get("ship")

        district = request.POST.get("district")

        if not f_name:
            error["First_name"] = "First name must be entered"
        if not l_name:
            error["last_name"] = "Last name must be entered"

        if not phone:
            error["Number"] = "Number must be entered"

        if not country:
            error["country"] = "country must be entered"
        if not state:
            error["state"] = "state must be entered"
        if not postalcode:
            error["postalcode"] = "postalcode must be entered"

        if not Address:
            error["Address"] = "Address must be entered"
        if not district:
            error["district"] = "Address must be entered"

        if not error:
            shipping_addds = shipping_address.objects.create(
                user=request.user,
                first_name=f_name,
                second_name=l_name,
                country=country,
                state=state,
                phone=phone,
                district=district,
                postal_code=postalcode,
                address=Address,
            )
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_addds,
                first_name=request.user.first_name,
            )

            all_total = 0
            for item in cart_item:
                t = 0
                total_tax = 0
                t += item.product.product_price * item.quantity

                if item.product.tax_rate:
                    total_tax = (t * item.product.tax_rate.rate) / 100
                    t += total_tax

                category_offer_var = CategoryOffer.objects.select_related(
                    "category"
                ).filter(category__Category_name=item.product.category.Category_name)

                if category_offer_var:
                    category_price_disc = 0

                    for i in category_offer_var:
                        category_price_disc += i.discount_percentage

                t -= category_price_disc
                all_total += t
                o = Orderitem.objects.create(
                    product=item.product,
                    shipping_option=shipping.objects.get(shipping_name=shipping_name),
                    order=order,
                    sub_total=item.product.product_price * item.quantity,
                    quantity=item.quantity,
                    total=t,
                )

            Order.objects.filter(id=order.pk).update(total=all_total)
            return redirect(
                reverse(
                    "userorder:bulk-buy-payment",
                    kwargs={"order_slug": order.slug, "o": o.slug},
                )
            )

    context = {
        "ship": ship,
        "t": round(t, 2),
        "errors": error,
        "cart_item": cart_item,
        "c": category_price_disc if category_price_disc != 0 else None,
    }
    return render(request, "userorder/checkout-bulk.html", context)


def bulk_buy_payment(request, order_slug, o):
    cart = Cart.objects.filter(user=request.user)
    order_item_to_shipping = Orderitem.objects.get(slug=o)

    t_tol = 0

    c = 0
    hi = 0
    for i in cart:
        t_tol += i.product.product_price * i.quantity
        c += 1
        if i.product.tax_rate:
            t_tol += t_tol * (i.product.tax_rate.rate / 100)

        category_offer_var = CategoryOffer.objects.select_related("category").filter(
            category__Category_name=i.product.category.Category_name
        )
        category_price_disc = 0
        if category_offer_var:
            for i in category_offer_var:
                hi += i.discount_percentage
                category_price_disc += i.discount_percentage

        t_tol -= category_price_disc
    c_open = Order.objects.filter(Q(slug=order_slug) & ~Q(coupon=None))
    coupen_to_add = 0
    if c_open:
        for i in c_open:
            coupen_to_add = i.coupon.discount_percentage

            total_discount = t_tol * (Decimal(coupen_to_add) / 100)
        t_tol -= total_discount

    t_tol += c * order_item_to_shipping.shipping_option.shipping_price

    sh_price = order_item_to_shipping.shipping_option.shipping_price
    request.session["total"] = float(t_tol)
    if request.method == "POST":
        payment = request.POST.get("payment")

        if not payment:
            messages.info(request, "Please select any of above")
            return redirect(
                reverse(
                    "userorder:bulk-buy-payment",
                    kwargs={"order_slug": order_slug, "o": o},
                )
            )
        else:
            if payment == "pay_by_wallet":
                w = wallet.objects.get(user=request.user)

                if float(w.balance) < t_tol:
                    messages.info(request, "Wallet money is not enough")
                    return redirect(
                        reverse(
                            "userorder:bulk-buy-payment",
                            kwargs={"order_slug": order_slug, "o": o},
                        )
                    )
                else:
                    Order.objects.filter(slug=order_slug).update(
                        payment_method=payment, paid=True, paid_amount=round(t_tol, 2)
                    )
                    w.balance -= t_tol
                    w.save()

                    request.session["order_slug"] = None
                    return redirect(reverse("userorder:payment-success-bulk"))

            if payment == "cash_on_delivery":
                Order.objects.filter(slug=order_slug).update(
                    payment_method=payment, paid=False, paid_amount=0
                )
                request.session["order_slug"] = None

                return redirect(reverse("userorder:payment-success-bulk"))
    di_o = Order.objects.filter(slug=order_slug).first()

    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": float(t_tol),
        "item_name": "cart_products",
        "invoice": str(di_o.pk),
        "currency_code": "USD",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('userorder:payment-success-bulk')}",
        "cancel_url": f"http://{host}{reverse('userorder:payment-failed')}",
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    Order.objects.filter(slug=order_slug).update(total=t_tol)

    request.session["order_slug"] = order_slug
    request.session["order_id"] = Order.objects.get(slug=order_slug).pk
    context = {
        "cart_item": cart,
        "form": form,
        "ot": o,
        "o": order_slug,
        "t": round(t_tol, 2),
        "sh_price": sh_price,
        "c_open": c_open,
        "c": hi if category_price_disc != 0 else None,
    }

    return render(request, "userorder/payment-bulkbuy.html", context)


def coupon_cart(request, o, order_slug):
    if request.method == "POST":
        coupon = request.POST["c"]
        if coupon:
            coupon_obj = Coupon.objects.filter(Q(code=coupon) & Q(active=True)).first()
            if coupon_obj:
                Order.objects.filter(slug=order_slug).update(
                    coupon=Coupon.objects.get(code=coupon)
                )

            else:
                messages.error(request, "Coupon has expired")
        else:
            messages.error(request, "Coupon has expired")

    return redirect(
        reverse("userorder:bulk-buy-payment", kwargs={"order_slug": order_slug, "o": o})
    )


@login_required(login_url="usermain:login")
def payment_success_cart(request):
    Cart.objects.filter(user=request.user).delete()

    order_slug = request.session.get("order_slug")
    if order_slug:
        order = get_object_or_404(Order, slug=order_slug)
        if order.paid_amount != 0:
            order.paid_amount = round(float(order.total), 2)
            order.paid = True
            order.payment_method = "paypal"
            order.save()

    request.session.pop("order_slug", None)
    total = request.session["total"]
    if request.GET.get("PayerID", ""):
        p = request.GET["PayerID"]
    else:
        p = None
    return render(
        request,
        "userorder/payment_succes.html",
        {"t": total, "order_id": request.session["order_id"], "PayerID": p},
    )


@login_required(login_url="usermain:login")
def payment_success(request):
    order_slug = request.session.get("order_slug")
    if order_slug:
        order = get_object_or_404(Order, slug=order_slug)

        if order.paid_amount != 0:
            order.paid_amount = round(float(order.total), 2)
            order.paid = True
            order.payment_method = "paypal"
            order.save()
    if request.session["cart_true"] == True:
        Cart.objects.filter(
            user=request.user,
            product=Products.objects.get(slug=request.session.get("pr_slug")),
        ).delete()

    request.session.pop("order_slug", None)
    request.session["input_value"] = None
    total = request.session["total"]
    if request.GET.get("PayerID", ""):
        p = request.GET["PayerID"]
    else:
        p = None
    return render(
        request,
        "userorder/payment_succes.html",
        {"t": round(total, 2), "order_id": request.session["order_id"], "PayerID": p},
    )


@login_required(login_url="usermain:login")
def payment_failed(request):
    request.session["input_value"] = None

    return render(request, "userorder/payment_failed.html")
