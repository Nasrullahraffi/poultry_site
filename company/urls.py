from django.urls import path
from company import views

app_name = 'company'

urlpatterns = [
    # Registration & Authentication
    path('register/', views.CompanyRegistrationView.as_view(), name='register'),
    path('login/', views.CompanyLoginView.as_view(), name='login'),
    path('logout/', views.CompanyLogoutView.as_view(), name='logout'),

    # Dashboard & Profile
    path('dashboard/', views.CompanyDashboardView.as_view(), name='dashboard'),
    path('profile/', views.CompanyProfileView.as_view(), name='profile'),

    # Legacy routes for backward compatibility
    path('registration/', views.CompanyRegView.as_view(), name='CompanyReg'),
]


