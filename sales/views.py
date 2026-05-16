from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from decimal import Decimal
from accounts.decorators import salesman_required
from accounts.models import CustomerProfile
from inventory.models import Medicine, StockTransaction
from .models import Cart, CartItem, Order, OrderItem, Payment, Return
from .forms import CheckoutForm, ReturnForm
from django.http import JsonResponse
from accounts.models import Company
from django.contrib import messages

def _get_or_create_open_cart(user):
    cart = Cart.objects.filter(user=user, status=Cart.OPEN).first()
    if not cart:
        cart = Cart.objects.create(user=user, status=Cart.OPEN)
    return cart

# @login_required
# @salesman_required
# def pos(request):
#     cart = _get_or_create_open_cart(request.user)
#     q = request.GET.get('q','').strip()
#     results = []
#     if q:
#         results = Medicine.objects.filter(Q(name__icontains=q) | Q(sku__icontains=q) | Q(barcode__icontains=q), is_active=True)[:25]
#     return render(request, 'sales/pos.html', {'cart': cart, 'results': results, 'q': q})

@login_required
@salesman_required
def pos(request):
    cart = _get_or_create_open_cart(request.user)
    q = request.GET.get('q', '').strip()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        results = []
        if q:
            meds = Medicine.objects.filter(
                # Q(name__icontains=q) | Q(sku__icontains=q) | Q(barcode__icontains=q),
                Q(name__icontains=q) | Q(gram__icontains=q) | Q(karate__icontains=q),
                is_active=True
            )[:25]
            results = [
                {
                    "id": m.id,
                    "name": m.name,
                    "gram": m.gram,
                    "karate": m.karate,
                    "price": m.selling_price,
                    "stock": m.quantity_in_stock,
                }
                for m in meds
            ]
        return JsonResponse({"results": results})
    else:
        
        # normal page render
        results = []

        results = Medicine.objects.filter(
            Q(name__icontains=q) | Q(gram__icontains=q) | Q(karate__icontains=q),
            is_active=True
        )[:25]
        results = [
            {
                "id": m.id,
                "name": m.name,
                "gram": m.gram,
                "karate": m.karate,
                "price": m.selling_price,
                "stock": m.quantity_in_stock,
            }
            for m in results
        ]
    return render(request, "sales/pos.html", {"cart": cart, "results": results, "q": q})


@login_required
@salesman_required
def add_to_cart(request, med_id):
    cart = _get_or_create_open_cart(request.user)
    med = get_object_or_404(Medicine, id=med_id, is_active=True)
    item, created = CartItem.objects.get_or_create(cart=cart, medicine=med, defaults={'quantity': 1, 'unit_price': med.selling_price})
    if not created:
        item.quantity += 1
        item.save()
    return redirect('sales:pos')

@login_required
@salesman_required
def remove_from_cart(request, item_id):
    cart = _get_or_create_open_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('sales:pos')

@login_required
@salesman_required
def update_quantity(request, item_id):
    cart = _get_or_create_open_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', '1'))
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()
    return redirect('sales:pos')


@login_required
@salesman_required
def checkout(request):
    cart = _get_or_create_open_cart(request.user)
    if not cart.items.exists():
        messages.warning(request, "Cart is empty. Please add items before checkout.")
        return redirect('sales:pos')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            discount = form.cleaned_data.get('discount') or Decimal('0.00')
            paid_amount = form.cleaned_data['paid_amount']
            payment_method = form.cleaned_data['payment_method']
            # karate = form.cleaned_data['karate'] 
            # gram = form.cleaned_data['gram']

            # Validate discount
            if discount > cart.subtotal:
                form.add_error('discount', 'Discount cannot exceed subtotal.')
                return render(request, 'sales/checkout.html', {'cart': cart, 'form': form})

            total = cart.subtotal - discount

            # Validate paid amount
            if paid_amount < total:
                form.add_error('paid_amount', 'Paid amount cannot be less than total.')
                return render(request, 'sales/checkout.html', {'cart': cart, 'form': form})

            with transaction.atomic():
                order = Order.objects.create(
                    order_type=order_type,
                    customer_profile=form.cleaned_data['customer'] if order_type == 'REGULAR' else None,
                    walk_in_name=form.cleaned_data['walk_in_name'] if order_type == 'WALKIN' else '',
                    walk_in_phone=form.cleaned_data['walk_in_phone'] if order_type == 'WALKIN' else '',
                    gram = form.cleaned_data['gram'],
                    karate = form.cleaned_data['karate'],
                    salesman=request.user,
                    subtotal=cart.subtotal,
                    discount=discount,
                    total=total,
                    status=Order.PAID,  # adjust if supporting partials
                )

                for ci in cart.items.select_related('medicine'):
                    # Lock the medicine row for update to avoid race conditions
                    med = Medicine.objects.select_for_update().get(pk=ci.medicine.pk)

                    if med.quantity_in_stock < ci.quantity:
                        transaction.set_rollback(True)
                        messages.error(request, f"Insufficient stock for {med.name}.")
                        return redirect('sales:pos')

                    med.quantity_in_stock -= ci.quantity
                    med.save()

                    StockTransaction.objects.create(
                        medicine=med,
                        type=StockTransaction.OUT,
                        quantity=ci.quantity,
                        note=f"Order#{order.id}",
                        created_by=request.user
                    )

                    OrderItem.objects.create(
                        order=order,
                        medicine=med,
                        gram = ci.medicine.gram,
                        karate = ci.medicine.karate,
                        quantity=ci.quantity,
                        unit_price=ci.unit_price,
                        cost_price=med.cost_price,
                    )

                Payment.objects.create(
                    order=order,
                    amount=paid_amount,
                    method=payment_method,
                    processed_by=request.user
                )

                cart.status = Cart.CHECKED_OUT
                cart.save()

            return redirect('sales:receipt', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'sales/checkout.html', {'cart': cart, 'form': form})


# @login_required
# @salesman_required
# def checkout(request):
#     cart = _get_or_create_open_cart(request.user)
#     if not cart.items.exists():
#         return redirect('sales:pos')
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             order_type = form.cleaned_data['order_type']
#             discount = form.cleaned_data.get('discount') or Decimal('0.00')
#             paid_amount = form.cleaned_data['paid_amount']
#             payment_method = form.cleaned_data['payment_method']

#             with transaction.atomic():
#                 order = Order.objects.create(
#                     order_type=order_type,
#                     customer_profile=form.cleaned_data['customer'] if order_type == 'REGULAR' else None,
#                     walk_in_name=form.cleaned_data['walk_in_name'] if order_type == 'WALKIN' else '',
#                     walk_in_phone=form.cleaned_data['walk_in_phone'] if order_type == 'WALKIN' else '',
#                     salesman=request.user,
#                     subtotal=cart.subtotal,
#                     discount=discount,
#                     total=cart.subtotal - discount,
#                     status=Order.PAID,
#                 )
#                 for ci in cart.items.select_related('medicine'):
#                     # reduce stock
#                     med = ci.medicine
#                     if med.quantity_in_stock < ci.quantity:
#                         messages.error(request, f"Insufficient stock for {med.name}")           
#                         return redirect('sales:pos')
#                     med.quantity_in_stock -= ci.quantity
#                     med.save()
#                     StockTransaction.objects.create(medicine=med, type=StockTransaction.OUT, quantity=ci.quantity, note=f"Order#{order.id}", created_by=request.user)

#                     OrderItem.objects.create(
#                         order=order,
#                         medicine=med,
#                         quantity=ci.quantity,
#                         unit_price=ci.unit_price,
#                         cost_price=med.cost_price,
#                     )
#                 Payment.objects.create(order=order, amount=paid_amount, method=payment_method, processed_by=request.user)
#                 cart.status = Cart.CHECKED_OUT
#                 cart.save()
#             return redirect('sales:receipt', order_id=order.id)
#     else:
#         form = CheckoutForm()
#     return render(request, 'sales/checkout.html', {'cart': cart, 'form': form})

@login_required
@salesman_required
def receipt(request, order_id):
    company = Company.objects.first()
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'sales/receipt.html', {'order': order, 'company': company})

@login_required
@salesman_required
def return_receipt(request, order_id):
    company = Company.objects.first()
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'sales/return_reciept.html', {'order': order, 'company': company})

@login_required
# @salesman_required
def return_orders_list(request):
    returns = Return.objects.order_by('-created_at')[:100]
    return render(request, 'sales/return_orders_list.html', {'returns': returns})

@login_required
# @salesman_required
def orders_list(request):
    orders = Order.objects.order_by('-created_at')[:100]
    return render(request, 'sales/orders_list.html', {'orders': orders})

@login_required
@salesman_required
def return_item(request, order_item_id):
    oi = get_object_or_404(OrderItem, id=order_item_id)
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            if qty > oi.quantity:
                qty = oi.quantity
            refund_amount = oi.unit_price * qty
            with transaction.atomic():
                # Restock
                med = oi.medicine
                med.quantity_in_stock += qty
                med.save()
                StockTransaction.objects.create(medicine=med, type=StockTransaction.RETURN_IN, quantity=qty, note=f"Return Order#{oi.order_id}", created_by=request.user)
                Return.objects.create(order_item=oi, quantity=qty, reason=reason, refund_amount=refund_amount, processed_by=request.user)
            return redirect('sales:receipt', order_id=oi.order_id)
    else:
        form = ReturnForm()
    return render(request, 'sales/return_form.html', {'form': form, 'order_item': oi})
