from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

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

# ---------------------------------------------------------------------------
# Batches
# ---------------------------------------------------------------------------
class BatchListView(LoginRequiredMixin, ListView):
    model = ChickBatch
    template_name = 'products/batch_list.html'
    context_object_name = 'batches'
    queryset = ChickBatch.objects.all().select_related()

class BatchCreateView(LoginRequiredMixin, CreateView):
    model = ChickBatch
    form_class = ChickBatchForm
    template_name = 'products/batch_form.html'

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, 'Batch created.')
        return redirect('batch_detail', pk=obj.pk)

class BatchDetailView(LoginRequiredMixin, DetailView):
    model = ChickBatch
    template_name = 'products/batch_detail.html'
    context_object_name = 'batch'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        batch = self.object
        ctx['health_checks'] = batch.health_checks.all()
        ctx['feed_schedules'] = batch.feed_schedules.select_related('formula').all()
        ctx['treatments'] = batch.treatments.select_related('medicine').all()
        ctx['disease_cases'] = batch.disease_cases.select_related('disease').all()
        ctx['rfid_tags'] = batch.rfid_tags.all()
        return ctx

# ---------------------------------------------------------------------------
# Health Check Create
# ---------------------------------------------------------------------------
class HealthCheckCreateView(LoginRequiredMixin, CreateView):
    model = HealthCheck
    form_class = HealthCheckForm
    template_name = 'products/healthcheck_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        hc = form.save(commit=False)
        hc.batch = self.batch
        hc.save()
        messages.success(self.request, 'Health check logged.')
        return redirect('batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Feed Formula List/Create & Feed Schedule Create
# ---------------------------------------------------------------------------
class FeedFormulaListView(LoginRequiredMixin, ListView):
    model = FeedFormula
    template_name = 'products/feed_formula_list.html'
    context_object_name = 'formulas'

class FeedFormulaCreateView(LoginRequiredMixin, CreateView):
    model = FeedFormula
    form_class = FeedFormulaForm
    template_name = 'products/feed_formula_form.html'
    success_url = reverse_lazy('feed_formula_list')

    def form_valid(self, form):
        messages.success(self.request, 'Feed formula created.')
        return super().form_valid(form)

class FeedScheduleCreateView(LoginRequiredMixin, CreateView):
    model = FeedSchedule
    form_class = FeedScheduleForm
    template_name = 'products/feed_schedule_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fs = form.save(commit=False)
        fs.batch = self.batch
        fs.save()
        messages.success(self.request, 'Feed schedule added.')
        return redirect('batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Medicine list/create & Treatment create
# ---------------------------------------------------------------------------
class MedicineListView(LoginRequiredMixin, ListView):
    model = MedicineProduct
    template_name = 'products/medicine_list.html'
    context_object_name = 'medicines'

class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = MedicineProduct
    form_class = MedicineProductForm
    template_name = 'products/medicine_form.html'
    success_url = reverse_lazy('medicine_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medicine added.')
        return super().form_valid(form)

class TreatmentCreateView(LoginRequiredMixin, CreateView):
    model = TreatmentRecord
    form_class = TreatmentRecordForm
    template_name = 'products/treatment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        tr = form.save(commit=False)
        tr.batch = self.batch
        tr.save()
        messages.success(self.request, 'Treatment recorded.')
        return redirect('batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Disease catalog list/create & case create
# ---------------------------------------------------------------------------
class DiseaseCatalogListView(LoginRequiredMixin, ListView):
    model = DiseaseCatalog
    template_name = 'products/disease_catalog_list.html'
    context_object_name = 'diseases'

class DiseaseCatalogCreateView(LoginRequiredMixin, CreateView):
    model = DiseaseCatalog
    form_class = DiseaseCatalogForm
    template_name = 'products/disease_catalog_form.html'
    success_url = reverse_lazy('disease_catalog_list')

    def form_valid(self, form):
        messages.success(self.request, 'Disease catalog entry added.')
        return super().form_valid(form)

class DiseaseCaseCreateView(LoginRequiredMixin, CreateView):
    model = DiseaseCase
    form_class = DiseaseCaseForm
    template_name = 'products/disease_case_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        dc = form.save(commit=False)
        dc.batch = self.batch
        dc.save()
        messages.success(self.request, 'Disease case logged.')
        return redirect('batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Inventory list/create & stock movement create
# ---------------------------------------------------------------------------
class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryProduct
    template_name = 'products/inventory_list.html'
    context_object_name = 'products'

class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'products/inventory_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Inventory product created.')
        return super().form_valid(form)

class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'products/stock_movement_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        sm = form.save()
        sm.apply()
        messages.success(self.request, 'Stock movement applied.')
        return redirect('inventory_list')

# ---------------------------------------------------------------------------
# Vendor list/create
# ---------------------------------------------------------------------------
class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'products/vendor_list.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        return Vendor.objects.filter(is_active=True)

class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'products/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vendor added.')
        return super().form_valid(form)

# ---------------------------------------------------------------------------
# Purchase Orders list/create with inline formset
# ---------------------------------------------------------------------------
class PurchaseOrderListView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'products/purchase_order_list.html'
    context_object_name = 'orders'
    queryset = PurchaseOrder.objects.select_related('vendor').all()

class PurchaseOrderCreateView(LoginRequiredMixin, View):
    template_name = 'products/purchase_order_form.html'

    def get(self, request):
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    @transaction.atomic
    def post(self, request):
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
        return render(request, self.template_name, {'form': form, 'formset': formset})

# ---------------------------------------------------------------------------
# RFID Tags list/create
# ---------------------------------------------------------------------------
class RFIDTagListView(LoginRequiredMixin, ListView):
    model = RFIDTag
    template_name = 'products/rfid_list.html'
    context_object_name = 'tags'

class RFIDTagCreateView(LoginRequiredMixin, CreateView):
    model = RFIDTag
    form_class = RFIDTagForm
    template_name = 'products/rfid_form.html'
    success_url = reverse_lazy('rfid_tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'RFID tag added.')
        return super().form_valid(form)
