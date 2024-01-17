from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import *
from usermain.models import Users
from django.db.models import *
from django.views.decorators.cache import never_cache
from userorder.models import Order, Orderitem
from django.http import JsonResponse, HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime


# Create your views here.
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adminhome:admin_panel")
    if request.method == "POST":
        email = request.POST["Email-log"]
        password = request.POST["Password-log"]
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("adminhome:admin_panel")
        else:
            messages.info(request, "Enter a valid user")
            return redirect("adminhome:admin_login")
    return render(request, "adminhome/Login.html")


@never_cache
def admin_panel(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")
    order_item = Orderitem.objects.all()
    pending = Orderitem.objects.filter(
        Q(order__status="pending") & ~Q(order__payment_method=None)
    ).aggregate(pending_order_count=Count("id"))
    user = Users.objects.filter(is_superuser=False).aggregate(Count("id"))
    t = 0
    for i in order_item:
        if i.total:
            t += float(i.total)

    return render(
        request,
        "adminhome/dashbord.html",
        {"t": round(t, 2), "p": pending["pending_order_count"], "u": user["id__count"]},
    )


def get_order_chart_data(request):
    orders = Order.objects.filter(~Q(payment_method=None) & Q(paid=True))

    series_data = []
    categories = []

    for order in orders:
        total_sales = order.order_items.aggregate(total_sales=Sum("sub_total"))[
            "total_sales"
        ]
        series_data.append(total_sales)
        categories.append(str(order.id))

    return JsonResponse(
        {"series_data": series_data, "categories": categories}, safe=False
    )


def admin_logout(request):
    logout(request)
    return redirect("adminhome:admin_login")


@never_cache
def customer(request):
    if request.user.is_superuser == False:
        return redirect("adminhome:admin_login")

    search = request.GET.get("search", "")

    if search:
        customer = Users.objects.filter(
            Q(first_name__icontains=search)
            | Q(email__icontains=search)
            | Q(Number__icontains=search),
            Q(is_superuser=False),
        )
    else:
        customer = Users.objects.filter(is_superuser=False)

    context = {"customer": customer}
    return render(request, "adminhome/customer.html", context)


def unblock_user(request, user_id):
    Users.objects.filter(id=user_id).update(is_blocked=False)

    return redirect(reverse("adminhome:customer"))


def block_user(request, user_id):
    Users.objects.filter(id=user_id).update(is_blocked=True)
    return redirect(reverse("adminhome:customer"))


def sales_report(request):
    orders = Orderitem.objects.select_related("order").filter(
        ~Q(order__payment_method=None)
    )
    request.session["start_date"] = None
    request.session["end_date"] = None
    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        if start_date > datetime.now() or end_date > datetime.now():
            return redirect(reverse("adminhome:sales-report"))
        orders = Orderitem.objects.select_related("order").filter(
            Q(order__created_at__range=[start_date, end_date])
            & ~Q(order__payment_method=None)
        )

        request.session["start_date"] = start_date_str
        request.session["end_date"] = end_date_str

    return render(request, "adminhome/sales.html", {"orders": orders})


def pdf_downlod(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [
        [
            "Order Number",
            "First Name",
            "Number",
            "Product name",
            "Item total",
            "Total Amount",
            "Order Date",
        ]
    ]
    if request.session.get("start_date") and request.session.get("end_date"):
        orders = Orderitem.objects.select_related("order").filter(
            Q(
                order__created_at__range=[
                    request.session.get("start_date"),
                    request.session.get("end_date"),
                ]
            )
            & ~Q(order__payment_method=None)
        )
    else:
        orders = Orderitem.objects.select_related("order").filter(
            ~Q(order__payment_method=None)
        )

    col_widths = [len(str(header)) for header in data[0]]
    for order in orders:
        user = order.order.user
        pr_nm = order.product.product_name[:27]
        row_data = [
            order.order.pk,
            user.first_name,
            user.Number,
            pr_nm,
            order.total,
            round(float(order.order.total), 2),
            order.order.created_at.strftime("%Y-%m-%d"),
        ]

        col_widths = [
            max(width, len(str(cell)) * 12) for width, cell in zip(col_widths, row_data)
        ]
        data.append(row_data)

    table = Table(data)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3F51B5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold", 3),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F0F8FF")),
            ("WORDWRAP", (0, 1), (-1, -1)),
        ]
    )

    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    return response
