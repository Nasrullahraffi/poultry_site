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
from company.models import Company


class CompanyScopedMixin:
    """Mixin to scope querysets to user's company"""

    def get_user_company(self):
        """Get the company associated with the current user"""
        user = self.request.user

        # Option 1: Direct ForeignKey from User to Company (most common)
        if hasattr(user, 'company') and user.company:
            return user.company

        # Option 2: Check if User has a company attribute (OneToOne or ForeignKey)
        try:
            return user.company
        except (AttributeError, Company.DoesNotExist):
            pass

        # Option 3: Try to find a company where user is the owner
        try:
            return Company.objects.get(owner=user)
        except (Company.DoesNotExist, AttributeError):
            pass

        # Option 4: Try to get through related name
        try:
            # If Company has a OneToOneField to User named 'user_profile'
            return Company.objects.get(user=user)
        except (Company.DoesNotExist, AttributeError):
            pass

        # Option 5: Check if user is associated with any company
        if hasattr(user, 'companies') and user.companies.exists():
            return user.companies.first()

        # Return None if no company found
        return None

    def get_queryset(self):
        qs = super().get_queryset()
        company = self.get_user_company()

        # Check if model has company field
        if hasattr(qs.model, 'company'):
            if company:
                return qs.filter(company=company)
            else:
                # If no company but model requires it, return empty queryset
                return qs.none()

        # If model doesn't have company field, return all (for global models)
        return qs

    def form_valid(self, form):
        """Automatically set company for Create/Update views"""
        if hasattr(form.instance, 'company'):
            company = self.get_user_company()
            if company:
                form.instance.company = company
            elif not form.instance.company:
                # If model requires company but user has none, raise error
                messages.error(self.request, 'You must be associated with a company to perform this action.')
                return self.form_invalid(form)
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
    success_url = reverse_lazy('products:batch_list')

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
    template_name = 'medicine/medicine_form.html'
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


class DiseaseCatalogCreateView(LoginRequiredMixin, CreateView):
    model = DiseaseCatalog
    form_class = DiseaseCatalogForm  # You need to create this form
    template_name = 'disease/disease_catalog_form.html'  # Different template
    success_url = reverse_lazy('products:disease_catalog_list')
    login_url = 'company:login'

    def form_valid(self, form):
        messages.success(self.request, 'Disease added to catalog.')
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




#--------------------------
# Inventory Views
# ---------------------------------------------------------------------------
class InventoryListView(LoginRequiredMixin, CompanyScopedMixin, ListView):
    model = InventoryProduct
    template_name = 'products/inventory_list.html'
    context_object_name = 'products'
    login_url = 'company:login'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get user's company
        company = self.get_user_company()

        # If company doesn't exist but model requires it, return empty queryset
        if hasattr(InventoryProduct, 'company') and not company:
            return queryset.none()

        # Apply filters
        status = self.request.GET.get('status')
        category = self.request.GET.get('category')

        if status == 'in_stock':
            queryset = queryset.filter(stock_on_hand__gt=0)
        elif status == 'low_stock':
            queryset = queryset.filter(stock_on_hand__gt=0).filter(
                stock_on_hand__lte=models.F('reorder_point')
            )
        elif status == 'out_of_stock':
            queryset = queryset.filter(stock_on_hand=0)

        if category:
            queryset = queryset.filter(category=category)

        # Only show active items by default, but allow seeing all if requested
        if not self.request.GET.get('show_inactive'):
            queryset = queryset.filter(is_active=True)

        return queryset.order_by('category', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        company = self.get_user_company()

        # Get all products for stats (unfiltered)
        all_products = super().get_queryset()

        # Filter by company if model has company field
        if hasattr(InventoryProduct, 'company') and company:
            all_products = all_products.filter(company=company)

        # Filter active products for stats
        all_active_products = all_products.filter(is_active=True)

        # Calculate stats
        in_stock = sum(1 for p in all_active_products if p.stock_on_hand > 0)
        low_stock = sum(1 for p in all_active_products if p.needs_reorder and p.stock_on_hand > 0)
        out_of_stock = sum(1 for p in all_active_products if p.stock_on_hand == 0)

        # Calculate total inventory value
        total_value = sum(
            (p.stock_on_hand * p.cost_price) for p in all_active_products
        )

        # Calculate margin for each product
        for product in products:
            if product.sale_price > 0 and product.cost_price > 0:
                margin = ((product.sale_price - product.cost_price) / product.cost_price) * 100
                product.margin_percentage = margin
            else:
                product.margin_percentage = 0

        context.update({
            'in_stock_count': in_stock,
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock,
            'reorder_count': low_stock,  # Same as low stock
            'categories_count': all_active_products.values('category').distinct().count(),
            'total_inventory_value': total_value,
            'category_choices': InventoryProduct._meta.get_field('category').choices,
            'user_company': company,  # Pass company to template
        })

        return context


class InventoryCreateView(LoginRequiredMixin, CompanyScopedMixin, CreateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'products/inventory_form.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def form_valid(self, form):
        # CompanyScopedMixin will handle setting the company
        messages.success(self.request, 'Inventory product created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_user_company()
        context['user_company'] = company

        # Show warning if no company
        if not company and hasattr(InventoryProduct, 'company'):
            messages.warning(self.request, 'You need to be associated with a company to add inventory items.')

        return context


class InventoryUpdateView(LoginRequiredMixin, CompanyScopedMixin, UpdateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'products/inventory_form.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def get_queryset(self):
        # Ensure users can only update their company's products
        qs = super().get_queryset()
        company = self.get_user_company()
        if company and hasattr(InventoryProduct, 'company'):
            return qs.filter(company=company)
        return qs

    def form_valid(self, form):
        messages.success(self.request, 'Inventory product updated successfully.')
        return super().form_valid(form)


class InventoryDeleteView(LoginRequiredMixin, CompanyScopedMixin, DeleteView):
    model = InventoryProduct
    template_name = 'products/inventory_confirm_delete.html'
    success_url = reverse_lazy('products:inventory_list')
    login_url = 'company:login'

    def get_queryset(self):
        # Ensure users can only delete their company's products
        qs = super().get_queryset()
        company = self.get_user_company()
        if company and hasattr(InventoryProduct, 'company'):
            return qs.filter(company=company)
        return qs

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Inventory product deleted.')
        return super().delete(request, *args, **kwargs)