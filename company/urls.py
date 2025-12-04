from django.urls import path
from company import views
from company.views import CompanyRegistrationView, CompanyLoginView, CompanyLogoutView, CompanyDashboardView, \
    CompanyProfileView, CompanyRegView

app_name = 'company'

urlpatterns = [

    path('register/', CompanyRegistrationView.as_view(), name='register'),
    path('login/', CompanyLoginView.as_view(), name='login'),
    path('logout/', CompanyLogoutView.as_view(), name='logout'),

    # Dashboard & Profile
    path('dashboard/', CompanyDashboardView.as_view(), name='dashboard'),
    path('profile/', CompanyProfileView.as_view(), name='profile'),

    # Legacy routes for backward compatibility
    path('registration/', CompanyRegView.as_view(), name='CompanyReg'),
]


