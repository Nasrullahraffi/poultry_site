from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models
from django.utils import timezone

from company.models import Company, CompanyMembership
from company.forms import CompanyRegistrationForm, CompanyProfileForm, LoginForm



class CompanyRegistrationView(View):
    """
    Handles user registration and company creation in one flow
    """
    template_name = 'company/company_registration.html'

    def get(self, request):
        # Redirect if already logged in
        if request.user.is_authenticated:
            return redirect('company:dashboard')

        form = CompanyRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Log the user in automatically after registration
            login(request, user)

            messages.success(
                request,
                f'Welcome! Your company account has been created successfully. '
                f'You can now start managing your poultry operations.'
            )
            return redirect('company:dashboard')

        return render(request, self.template_name, {'form': form})


class CompanyLoginView(LoginView):
    """
    Custom login view for company users
    """
    template_name = 'company/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('company:dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)


class CompanyLogoutView(LogoutView):
    """
    Custom logout view - shows confirmation page on GET, logs out on POST
    Redirects to login page after logout
    """
    template_name = 'company/logout.html'
    next_page = 'company:login'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated:
            messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class CompanyDashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard for company users showing overview of operations
    """
    template_name = 'company/company_dashboard.html'
    login_url = 'company:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user's active company membership
        membership = CompanyMembership.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('company').first()

        if membership:
            company = membership.company
            context['company'] = company
            context['membership'] = membership

            # Get company statistics
            from products.models import ChickBatch, InventoryProduct, ChickStatus

            # Basic stats
            all_batches = ChickBatch.objects.filter(company=company)
            active_batches = all_batches.filter(status=ChickStatus.ACTIVE)

            # Calculate total chicks for active batches
            total_chicks = 0
            for batch in active_batches:
                total_chicks += batch.current_count if batch.current_count is not None else batch.initial_count

            context['stats'] = {
                'total_batches': all_batches.count(),
                'active_batches': active_batches.count(),
                'total_chicks': total_chicks,
                'inventory_items': InventoryProduct.objects.filter(
                    company=company,
                    is_active=True
                ).count(),
                'low_stock_items': InventoryProduct.objects.filter(
                    company=company,
                    is_active=True,
                    stock_on_hand__lte=models.F('reorder_point')
                ).count() if InventoryProduct.objects.filter(company=company).exists() else 0,
            }

            # Enhanced performance metrics
            if active_batches.exists():
                today = timezone.now().date()

                # Calculate average batch age
                total_age = 0
                valid_batches = 0
                for batch in active_batches:
                    if batch.hatch_date:
                        age_days = (today - batch.hatch_date).days
                        total_age += age_days
                        valid_batches += 1

                if valid_batches > 0:
                    context['stats']['avg_batch_age'] = total_age // valid_batches

                # Calculate mortality rate
                total_initial = sum(batch.initial_count for batch in active_batches)
                total_current = 0
                for batch in active_batches:
                    total_current += batch.current_count if batch.current_count is not None else batch.initial_count

                if total_initial > 0:
                    mortality_rate = ((total_initial - total_current) / total_initial) * 100
                    context['stats']['mortality_rate'] = round(mortality_rate, 1)

                # Oldest active batch age
                oldest_batch = None
                for batch in active_batches:
                    if batch.hatch_date:
                        if oldest_batch is None or batch.hatch_date < oldest_batch.hatch_date:
                            oldest_batch = batch

                if oldest_batch and oldest_batch.hatch_date:
                    context['stats']['oldest_active_batch'] = (today - oldest_batch.hatch_date).days

            # Recent activity simulation
            context['recent_activities'] = self.get_recent_activities(company)

            # Alerts and notifications
            context['alerts'] = self.get_alerts(company)
            context['alerts_count'] = len(context['alerts'])

            # Recent batches (age_days is already calculated via @property in model)
            recent_batches = all_batches.select_related().order_by('-created_at')[:5]


            context['recent_batches'] = recent_batches

        else:
            context['company'] = None
            messages.warning(
                self.request,
                'You are not associated with any company. Please contact support.'
            )

        return context

    def get_recent_activities(self, company):
        """Get recent activities for the company"""
        activities = []

        # Check for recent batch creations
        from products.models import ChickBatch
        recent_batches = ChickBatch.objects.filter(
            company=company,
            created_at__gte=timezone.now() - timedelta(days=1)
        )[:3]

        for batch in recent_batches:
            activities.append({
                'icon': 'plus-circle',
                'color': 'success',
                'message': f'New batch #{batch.id} created',
                'timestamp': batch.created_at
            })

        # Check for low inventory
        from products.models import InventoryProduct
        low_stock = InventoryProduct.objects.filter(
            company=company,
            stock_on_hand__lte=models.F('reorder_point'),
            is_active=True
        )[:2]

        for item in low_stock:
            activities.append({
                'icon': 'exclamation-triangle',
                'color': 'warning',
                'message': f'Low stock: {item.name}',
                'timestamp': timezone.now() - timedelta(hours=2)
            })

        return activities

    def get_alerts(self, company):
        """Get current alerts for the company"""
        alerts = []

        # Check for batches needing attention
        from products.models import ChickBatch, ChickStatus
        active_batches = ChickBatch.objects.filter(
            company=company,
            status=ChickStatus.ACTIVE
        )

        today = timezone.now().date()

        for batch in active_batches:
            # Calculate current count safely
            current_count = batch.current_count if batch.current_count is not None else batch.initial_count

            # Check for high mortality (more than 10% loss)
            if current_count < batch.initial_count * 0.9:
                alerts.append({
                    'priority': 'high',
                    'title': 'High Mortality Rate',
                    'message': f'Batch #{batch.id} has significant losses'
                })

            # Check for old batches (older than 365 days)
            if batch.hatch_date:
                age_days = (today - batch.hatch_date).days
                if age_days > 365:
                    alerts.append({
                        'priority': 'medium',
                        'title': 'Batch Aging',
                        'message': f'Batch #{batch.id} is over 1 year old'
                    })

        # Check for critical low inventory
        from products.models import InventoryProduct
        critical_stock = InventoryProduct.objects.filter(
            company=company,
            stock_on_hand=0,  # Completely out of stock
            is_active=True
        )

        for item in critical_stock:
            alerts.append({
                'priority': 'high',
                'title': 'Out of Stock',
                'message': f'{item.name} is completely out of stock'
            })

        return alerts
class CompanyProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating company profile
    """
    model = Company
    form_class = CompanyProfileForm
    template_name = 'company/company_profile.html'
    login_url = 'company:login'
    success_url = reverse_lazy('company:dashboard')

    def get_object(self, queryset=None):
        # Get the company for the logged-in user
        membership = get_object_or_404(
            CompanyMembership,
            user=self.request.user,
            is_active=True
        )
        return membership.company

    def form_valid(self, form):
        messages.success(self.request, 'Company profile updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_object()
        return context


# Legacy view - kept for backward compatibility
class CompanyRegView(View):
    """
    Legacy registration view - redirects to new flow
    """
    def get(self, request):
        return redirect('company:register')

    def post(self, request):
        return redirect('company:register')



