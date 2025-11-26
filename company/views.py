from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models

from company.models import Company, CompanyMembership
from company.forms import CompanyRegistrationForm, CompanyProfileForm, LoginForm


class CompanyRegistrationView(View):
    """
    Handles user registration and company creation in one flow
    """
    template_name = 'company/registration.html'

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
    Custom logout view
    """
    next_page = 'major:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class CompanyDashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard for company users showing overview of operations
    """
    template_name = 'company/dashboard.html'
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

            context['stats'] = {
                'total_batches': ChickBatch.objects.filter(company=company).count(),
                'active_batches': ChickBatch.objects.filter(
                    company=company,
                    status=ChickStatus.ACTIVE
                ).count(),
                'total_chicks': sum(
                    batch.current_count or batch.initial_count
                    for batch in ChickBatch.objects.filter(
                        company=company,
                        status=ChickStatus.ACTIVE
                    )
                ),
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

            # Recent activity
            context['recent_batches'] = ChickBatch.objects.filter(
                company=company
            ).select_related().order_by('-created_at')[:5]

        else:
            context['company'] = None
            messages.warning(
                self.request,
                'You are not associated with any company. Please contact support.'
            )

        return context


class CompanyProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating company profile
    """
    model = Company
    form_class = CompanyProfileForm
    template_name = 'company/profile.html'
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



