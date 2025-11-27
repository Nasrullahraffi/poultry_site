from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import (
    ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct
)
from products.forms import (
    ChickBatchForm, HealthCheckForm, FeedFormulaForm, FeedScheduleForm,
    MedicineProductForm, TreatmentRecordForm, DiseaseCatalogForm, DiseaseCaseForm,
    InventoryProductForm
)
from company.models import CompanyMembership


class CompanyScopedMixin:
    """
    Mixin to automatically scope querysets to user's company
    """
    def get_user_company(self):
        """Get the active company for the logged-in user"""
        membership = CompanyMembership.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('company').first()

        if not membership:
            messages.error(self.request, 'You are not associated with any active company.')
            return None

        return membership.company

    def get_queryset(self):
        """Filter queryset by user's company"""
        qs = super().get_queryset()
        company = self.get_user_company()

        if company and hasattr(qs.model, 'company'):
            return qs.filter(company=company)
        return qs

    def form_valid(self, form):
        """Automatically set company on form save"""
        company = self.get_user_company()

        if not company:
            messages.error(self.request, 'Cannot save: No active company found.')
            return redirect('company:dashboard')

        if hasattr(form.instance, 'company'):
            form.instance.company = company

        return super().form_valid(form)

# ---------------------------------------------------------------------------
# Batches
# ---------------------------------------------------------------------------
class BatchListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = ChickBatch
    template_name = 'batch/batch_list.html'
    context_object_name = 'batches'
    login_url = 'company:login'

class BatchCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = ChickBatch
    form_class = ChickBatchForm
    template_name = 'batch/batch_form.html'
    success_url = reverse_lazy('products:batch_list')
    login_url = 'company:login'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Batch created.')
        return redirect('products:batch_detail', pk=self.object.pk)

class BatchDetailView(LoginRequiredMixin, CompanyScopedMixin, DetailView):
    model = ChickBatch
    template_name = 'batch/batch_detail.html'
    context_object_name = 'batch'
    login_url = 'company:login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        batch = self.object
        ctx['health_checks'] = batch.health_checks.all()
        ctx['feed_schedules'] = batch.feed_schedules.select_related('formula').all()
        ctx['treatments'] = batch.treatments.select_related('medicine').all()
        ctx['disease_cases'] = batch.disease_cases.select_related('disease').all()
        return ctx

class BatchUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = ChickBatch
    form_class = ChickBatchForm
    template_name = 'batch/batch_form.html'
    login_url = 'company:login'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Batch updated.')
        return redirect('products:batch_detail', pk=self.object.pk)

class BatchDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = ChickBatch
    template_name = 'batch/batch_confirm_delete.html'
    success_url = reverse_lazy('products:batch_list')
    login_url = 'company:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Batch deleted.')
        return super().delete(request, *args, **kwargs)

# ---------------------------------------------------------------------------
# Health Check Create
# ---------------------------------------------------------------------------
class HealthCheckCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = HealthCheck
    form_class = HealthCheckForm
    template_name = 'products/healthcheck_form.html'
    login_url = 'company:login'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        # Verify batch belongs to user's company
        company = self.get_user_company()
        if company and self.batch.company != company:
            messages.error(request, 'Access denied: This batch does not belong to your company.')
            return redirect('company:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        hc = form.save(commit=False)
        hc.batch = self.batch
        hc.save()
        messages.success(self.request, 'Health check logged.')
        return redirect('products:batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Feed Formula List/Create & Feed Schedule Create
# ---------------------------------------------------------------------------
class FeedFormulaListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = FeedFormula
    template_name = 'products/feed_formula_list.html'
    context_object_name = 'formulas'
    login_url = 'company:login'

class FeedFormulaCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = FeedFormula
    form_class = FeedFormulaForm
    template_name = 'products/feed_formula_form.html'
    success_url = reverse_lazy('products:feed_formula_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Feed formula created.')
        return super().form_valid(form)

class FeedScheduleCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = FeedSchedule
    form_class = FeedScheduleForm
    template_name = 'products/feed_schedule_form.html'
    login_url = 'company:login'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        # Verify batch belongs to user's company
        company = self.get_user_company()
        if company and self.batch.company != company:
            messages.error(request, 'Access denied: This batch does not belong to your company.')
            return redirect('company:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fs = form.save(commit=False)
        fs.batch = self.batch
        fs.save()
        messages.success(self.request, 'Feed schedule added.')
        return redirect('products:batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx


class FeedFormulaUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = FeedFormula
    form_class = FeedFormulaForm
    template_name = 'products/feed_formula_form.html'
    success_url = reverse_lazy('products:feed_formula_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Feed formula updated.')
        return super().form_valid(form)

class FeedFormulaDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = FeedFormula
    template_name = 'products/feed_formula_confirm_delete.html'
    success_url = reverse_lazy('products:feed_formula_list')
    login_url = 'company:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Feed formula deleted.')
        return super().delete(request, *args, **kwargs)



# ---------------------------------------------------------------------------
# Medicine list/create & Treatment create
# ---------------------------------------------------------------------------
class MedicineListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = MedicineProduct
    template_name = 'medicine/medicine_list.html'
    context_object_name = 'medicines'
    login_url = 'company:login'

class MedicineCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = MedicineProduct
    form_class = MedicineProductForm
    template_name = 'medicine/medicine_form.html'
    success_url = reverse_lazy('products:medicine_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Medicine added.')
        return super().form_valid(form)

class MedicineUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = MedicineProduct
    form_class = MedicineProductForm
    template_name = 'products/templates/medicine/medicine_form.html'
    success_url = reverse_lazy('products:medicine_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Medicine updated.')
        return super().form_valid(form)

class MedicineDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = MedicineProduct
    template_name = 'medicine/medicine_confirm_delete.html'
    success_url = reverse_lazy('products:medicine_list')
    login_url = 'company:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Medicine deleted.')
        return super().delete(request, *args, **kwargs)



class TreatmentCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = TreatmentRecord
    form_class = TreatmentRecordForm
    template_name = 'products/treatment_form.html'
    login_url = 'company:login'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        # Verify batch belongs to user's company
        company = self.get_user_company()
        if company and self.batch.company != company:
            messages.error(request, 'Access denied: This batch does not belong to your company.')
            return redirect('company:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        tr = form.save(commit=False)
        tr.batch = self.batch
        tr.save()
        messages.success(self.request, 'Treatment recorded.')
        return redirect('products:batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Disease catalog list/create & case create
# ---------------------------------------------------------------------------
class DiseaseCatalogListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = DiseaseCatalog
    template_name = 'disease/disease_catalog_list.html'
    context_object_name = 'diseases'
    login_url = 'company:login'



class DiseaseCatalogUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = DiseaseCatalog
    form_class = DiseaseCatalogForm
    template_name = 'disease/disease_catalog_form.html'
    success_url = reverse_lazy('products:disease_catalog_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Disease catalog entry updated.')
        return super().form_valid(form)

class DiseaseCatalogDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = DiseaseCatalog
    template_name = 'disease/disease_catalog_confirm_delete.html'
    success_url = reverse_lazy('products:disease_catalog_list')
    login_url = 'company:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Disease catalog entry deleted.')
        return super().delete(request, *args, **kwargs)


class DiseaseCatalogCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = DiseaseCatalog
    form_class = DiseaseCatalogForm
    template_name = 'disease/disease_catalog_form.html'
    success_url = reverse_lazy('products:disease_catalog_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Disease catalog entry added.')
        return super().form_valid(form)

class DiseaseCaseCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = DiseaseCase
    form_class = DiseaseCaseForm
    template_name = 'disease/disease_case_form.html'
    login_url = 'company:login'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(ChickBatch, pk=kwargs['batch_pk'])
        # Verify batch belongs to user's company
        company = self.get_user_company()
        if company and self.batch.company != company:
            messages.error(request, 'Access denied: This batch does not belong to your company.')
            return redirect('company:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        dc = form.save(commit=False)
        dc.batch = self.batch
        dc.save()
        messages.success(self.request, 'Disease case logged.')
        return redirect('products:batch_detail', pk=self.batch.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['batch'] = self.batch
        return ctx

# ---------------------------------------------------------------------------
# Inventory list/create
# ---------------------------------------------------------------------------



#--------------------------
# Inventory Views
# ---------------------------------------------------------------------------
class InventoryListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = InventoryProduct
    template_name = 'products/inventory_list.html'
    context_object_name = 'products'
    login_url = 'company:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        # Calculate stats
        context['in_stock_count'] = sum(1 for p in products if p.stock_on_hand > 0)
        context['low_stock_count'] = sum(1 for p in products if p.needs_reorder)
        context['out_of_stock_count'] = sum(1 for p in products if p.stock_on_hand == 0)
        context['reorder_count'] = sum(1 for p in products if p.needs_reorder)
        context['categories_count'] = products.values('category').distinct().count() if products else 0

        return context

class InventoryCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'products/inventory_form.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Inventory product created.')
        return super().form_valid(form)


class InventoryUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'products/inventory_form.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Inventory product updated.')
        return super().form_valid(form)

class InventoryDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = InventoryProduct
    template_name = 'products/inventory_confirm_delete.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Inventory product deleted.')
        return super().delete(request, *args, **kwargs)
