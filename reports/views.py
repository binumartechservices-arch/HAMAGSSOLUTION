# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from accounts.decorators import admin_required, salesman_required
# from django.utils import timezone
# from datetime import timedelta
# from django.db.models import Sum, F
# from sales.models import Order, OrderItem, Payment
# from inventory.models import Medicine

# def _range_dates(kind: str):
#     now = timezone.now()
#     if kind == 'daily':
#         start = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     elif kind == 'weekly':
#         start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
#     elif kind == 'monthly':
#         start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     elif kind == 'yearly':
#         start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
#     else:
#         start = now - timedelta(days=30)
#     return start, now

# @login_required
# @admin_required
# def admin_dashboard(request):
#     kind = request.GET.get('range','daily')
#     start, end = _range_dates(kind)
#     orders = Order.objects.filter(created_at__range=(start, end))
#     payments = Payment.objects.filter(created_at__range=(start, end))

#     sales_total = orders.aggregate(s=Sum('total'))['s'] or 0
#     paid_total = payments.aggregate(s=Sum('amount'))['s'] or 0
#     profit_total = OrderItem.objects.filter(order__in=orders).aggregate(
#         p=Sum((F('unit_price') - F('cost_price')) * F('quantity'))
#     )['p'] or 0

#     low_stock = Medicine.objects.filter(quantity_in_stock__lte=F('reorder_level'))[:20]

#     context = {
#         'kind': kind,
#         'sales_total': sales_total,
#         'paid_total': paid_total,
#         'profit_total': profit_total,
#         'low_stock': low_stock,
#         'orders': orders.order_by('-created_at')[:20],
#     }
#     return render(request, 'reports/admin_dashboard.html', context)

# @login_required
# @salesman_required
# def salesman_dashboard(request):
#     kind = request.GET.get('range','daily')
#     start, end = _range_dates(kind)
#     orders = Order.objects.filter(salesman=request.user, created_at__range=(start, end))
#     payments = Payment.objects.filter(processed_by=request.user, created_at__range=(start, end))
#     sales_total = orders.aggregate(s=Sum('total'))['s'] or 0
#     paid_total = payments.aggregate(s=Sum('amount'))['s'] or 0
#     profit_total = 0
#     context = {
#         'kind': kind,
#         'sales_total': sales_total,
#         'paid_total': paid_total,
#         'orders': orders.order_by('-created_at')[:50],
#     }
#     return render(request, 'reports/salesman_dashboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, salesman_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F
from sales.models import Order, OrderItem, Payment, Return
from inventory.models import Medicine


def _range_dates(kind: str):
    now = timezone.now()
    if kind == 'today':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif kind == 'weekly':
        start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    elif kind == 'monthly':
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif kind == 'yearly':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start = now - timedelta(days=30)
    return start, now


@login_required
@admin_required
def admin_dashboard(request):
    kind = request.GET.get("range", "today")
    start, end = _range_dates(kind)

    orders = Order.objects.filter(created_at__range=(start, end))
    payments = Payment.objects.filter(created_at__range=(start, end))
    returns = Return.objects.filter(created_at__range=(start, end))

    sales_total = orders.aggregate(s=Sum("total"))["s"] or 0
    paid_total = payments.aggregate(s=Sum("amount"))["s"] or 0
    returns_total = returns.aggregate(r=Sum("refund_amount"))["r"] or 0
    net_sales = sales_total - returns_total

    profit_total = (
        OrderItem.objects.filter(order__in=orders).aggregate(
            p=Sum((F("unit_price") - F("cost_price")) * F("quantity"))
        )["p"]
        or 0
    )

    low_stock = Medicine.objects.filter(quantity_in_stock__lte=F("reorder_level"))[:20]

    context = {
        "kind": kind,
        "sales_total": sales_total,
        "paid_total": paid_total,
        "returns_total": returns_total,
        "net_sales": net_sales,
        "profit_total": profit_total,
        "low_stock": low_stock,
        "orders": orders.order_by("-created_at")[:20],
        "returns": returns.order_by("-created_at")[:20],
    }
    return render(request, "reports/admin_dashboard.html", context)


@login_required
@salesman_required
def salesman_dashboard(request):
    kind = request.GET.get("range", "daily")
    start, end = _range_dates(kind)

    orders = Order.objects.filter(
        salesman=request.user, created_at__range=(start, end)
    )
    payments = Payment.objects.filter(
        processed_by=request.user, created_at__range=(start, end)
    )
    returns = Return.objects.filter(
        processed_by=request.user, created_at__range=(start, end)
    )

    sales_total = orders.aggregate(s=Sum("total"))["s"] or 0
    paid_total = payments.aggregate(s=Sum("amount"))["s"] or 0
    returns_total = returns.aggregate(r=Sum("refund_amount"))["r"] or 0
    net_sales = sales_total - returns_total

    context = {
        "kind": kind,
        "sales_total": sales_total,
        "paid_total": paid_total,
        "returns_total": returns_total,
        "net_sales": net_sales,
        "orders": orders.order_by("-created_at")[:50],
        "returns": returns.order_by("-created_at")[:50],
    }
    return render(request, "reports/salesman_dashboard.html", context)
