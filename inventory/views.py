from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from .models import Medicine, StockTransaction
from .forms import MedicineForm
from django.contrib import messages

@login_required
@admin_required
def medicine_list(request):
    q = request.GET.get('q','').strip()
    meds = Medicine.objects.all().order_by('name')
    if q:
        meds = meds.filter(name__icontains=q)
    
    low_stock_only = request.GET.get('low') == '1'
    if low_stock_only:
        meds = [m for m in meds if m.low_stock]
    return render(request, 'inventory/medicine_list.html', {'medicines': meds, 'q': q, 'low': low_stock_only})

@login_required
@admin_required
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            med = form.save()
            messages.success(request, "Medicine added successfully.")
            if med.quantity_in_stock:
                StockTransaction.objects.create(medicine=med, type=StockTransaction.IN, quantity=med.quantity_in_stock, note='Initial stock', created_by=request.user)
            return redirect('inventory:medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'inventory/medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
@admin_required
def medicine_update(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    old_qty = med.quantity_in_stock
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=med)
        if form.is_valid():
            med = form.save()
            diff = med.quantity_in_stock - old_qty
            if diff != 0:
                StockTransaction.objects.create(medicine=med, type=StockTransaction.ADJUST, quantity=diff, note='Manual adjust', created_by=request.user)
            return redirect('inventory:medicine_list')
    else:
        form = MedicineForm(instance=med)
    return render(request, 'inventory/medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

@login_required
@admin_required
def medicine_delete(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        med.delete()
        return redirect('inventory:medicine_list')
    return render(request, 'inventory/medicine_confirm_delete.html', {'medicine': med})
