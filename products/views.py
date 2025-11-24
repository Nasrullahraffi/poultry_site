from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from products.models import (
    ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct, StockMovement, Vendor, PurchaseOrder, PurchaseOrderItem,
    RFIDTag
)
from products.forms import (
    ChickBatchForm, HealthCheckForm, FeedFormulaForm, FeedScheduleForm,
    MedicineProductForm, TreatmentRecordForm, DiseaseCatalogForm, DiseaseCaseForm,
    InventoryProductForm, StockMovementForm, VendorForm, PurchaseOrderForm,
    PurchaseOrderItemFormSet, RFIDTagForm
)

# --------------------------------------------------------------
# Utility
# --------------------------------------------------------------

def _save_form(request, form, success_msg):
    if form.is_valid():
        obj = form.save()
        messages.success(request, success_msg)
        return obj
    return None

# --------------------------------------------------------------
# Chick Batches
# --------------------------------------------------------------
@login_required
def batch_list(request):
    batches = ChickBatch.objects.select_related().all()
    return render(request, 'products/batch_list.html', {'batches': batches})

@login_required
def batch_create(request):
    if request.method == 'POST':
        form = ChickBatchForm(request.POST)
        obj = _save_form(request, form, 'Batch created.')
        if obj:
            return redirect('batch_detail', pk=obj.pk)
    else:
        form = ChickBatchForm()
    return render(request, 'products/batch_form.html', {'form': form})

@login_required
def batch_detail(request, pk):
    batch = get_object_or_404(ChickBatch, pk=pk)
    health_checks = batch.health_checks.all()
    feed_schedules = batch.feed_schedules.select_related('formula').all()
    treatments = batch.treatments.select_related('medicine').all()
    disease_cases = batch.disease_cases.select_related('disease').all()
    rfid_tags = batch.rfid_tags.all()
    return render(request, 'products/batch_detail.html', {
        'batch': batch,
        'health_checks': health_checks,
        'feed_schedules': feed_schedules,
        'treatments': treatments,
        'disease_cases': disease_cases,
        'rfid_tags': rfid_tags,
    })

# --------------------------------------------------------------
# Health Checks
# --------------------------------------------------------------
@login_required
def health_check_add(request, batch_pk):
    batch = get_object_or_404(ChickBatch, pk=batch_pk)
    if request.method == 'POST':
        form = HealthCheckForm(request.POST)
        if form.is_valid():
            hc = form.save(commit=False)
            hc.batch = batch
            hc.save()
            messages.success(request, 'Health check logged.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = HealthCheckForm()
    return render(request, 'products/healthcheck_form.html', {'form': form, 'batch': batch})

# --------------------------------------------------------------
# Feed Formula & Scheduling
# --------------------------------------------------------------
@login_required
def feed_formula_list(request):
    formulas = FeedFormula.objects.all()
    return render(request, 'products/feed_formula_list.html', {'formulas': formulas})

@login_required
def feed_formula_create(request):
    if request.method == 'POST':
        form = FeedFormulaForm(request.POST)
        obj = _save_form(request, form, 'Feed formula created.')
        if obj:
            return redirect('feed_formula_list')
    else:
        form = FeedFormulaForm()
    return render(request, 'products/feed_formula_form.html', {'form': form})

@login_required
def feed_schedule_add(request, batch_pk):
    batch = get_object_or_404(ChickBatch, pk=batch_pk)
    if request.method == 'POST':
        form = FeedScheduleForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.batch = batch
            fs.save()
            messages.success(request, 'Feed schedule added.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = FeedScheduleForm()
    return render(request, 'products/feed_schedule_form.html', {'form': form, 'batch': batch})

# --------------------------------------------------------------
# Medicine & Treatments
# --------------------------------------------------------------
@login_required
def medicine_list(request):
    meds = MedicineProduct.objects.all()
    return render(request, 'products/medicine_list.html', {'medicines': meds})

@login_required
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineProductForm(request.POST)
        obj = _save_form(request, form, 'Medicine added.')
        if obj:
            return redirect('medicine_list')
    else:
        form = MedicineProductForm()
    return render(request, 'products/medicine_form.html', {'form': form})

@login_required
def treatment_add(request, batch_pk):
    batch = get_object_or_404(ChickBatch, pk=batch_pk)
    if request.method == 'POST':
        form = TreatmentRecordForm(request.POST)
        if form.is_valid():
            tr = form.save(commit=False)
            tr.batch = batch
            tr.save()
            messages.success(request, 'Treatment recorded.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = TreatmentRecordForm()
    return render(request, 'products/treatment_form.html', {'form': form, 'batch': batch})

# --------------------------------------------------------------
# Disease Catalog & Cases
# --------------------------------------------------------------
@login_required
def disease_catalog_list(request):
    diseases = DiseaseCatalog.objects.all()
    return render(request, 'products/disease_catalog_list.html', {'diseases': diseases})

@login_required
def disease_catalog_create(request):
    if request.method == 'POST':
        form = DiseaseCatalogForm(request.POST)
        obj = _save_form(request, form, 'Disease catalog entry added.')
        if obj:
            return redirect('disease_catalog_list')
    else:
        form = DiseaseCatalogForm()
    return render(request, 'products/disease_catalog_form.html', {'form': form})

@login_required
def disease_case_add(request, batch_pk):
    batch = get_object_or_404(ChickBatch, pk=batch_pk)
    if request.method == 'POST':
        form = DiseaseCaseForm(request.POST)
        if form.is_valid():
            dc = form.save(commit=False)
            dc.batch = batch
            dc.save()
            messages.success(request, 'Disease case logged.')
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = DiseaseCaseForm()
    return render(request, 'products/disease_case_form.html', {'form': form, 'batch': batch})

# --------------------------------------------------------------
# Inventory & Stock
# --------------------------------------------------------------
@login_required
def inventory_list(request):
    products = InventoryProduct.objects.all()
    return render(request, 'products/inventory_list.html', {'products': products})

@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryProductForm(request.POST)
        obj = _save_form(request, form, 'Inventory product created.')
        if obj:
            return redirect('inventory_list')
    else:
        form = InventoryProductForm()
    return render(request, 'products/inventory_form.html', {'form': form})

@login_required
def stock_movement_add(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            sm = form.save()
            sm.apply()
            messages.success(request, 'Stock movement applied.')
            return redirect('inventory_list')
    else:
        form = StockMovementForm()
    return render(request, 'products/stock_movement_form.html', {'form': form})

# --------------------------------------------------------------
# Vendors & Purchase Orders
# --------------------------------------------------------------
@login_required
def vendor_list(request):
    vendors = Vendor.objects.filter(is_active=True)
    return render(request, 'products/vendor_list.html', {'vendors': vendors})

@login_required
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        obj = _save_form(request, form, 'Vendor added.')
        if obj:
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'products/vendor_form.html', {'form': form})

@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.select_related('vendor').all()
    return render(request, 'products/purchase_order_list.html', {'orders': orders})

@login_required
@transaction.atomic
def purchase_order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            po = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.purchase_order = po
                item.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'Purchase order created.')
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
    return render(request, 'products/purchase_order_form.html', {'form': form, 'formset': formset})

# --------------------------------------------------------------
# RFID Tags
# --------------------------------------------------------------
@login_required
def rfid_tag_list(request):
    tags = RFIDTag.objects.all()
    return render(request, 'products/rfid_list.html', {'tags': tags})

@login_required
def rfid_tag_create(request):
    if request.method == 'POST':
        form = RFIDTagForm(request.POST)
        obj = _save_form(request, form, 'RFID tag added.')
        if obj:
            return redirect('rfid_tag_list')
    else:
        form = RFIDTagForm()
    return render(request, 'products/rfid_form.html', {'form': form})
