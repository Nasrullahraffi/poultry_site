from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from company.forms import *

urlpatterns = [
    path("sign", views.companyView, name="company"),
    path('accounts/login',auth_view.LoginView.as_view(template_name='company/login.html', authentication_form=Login_Form), name='login'),
    path('registration/', views.CompanyRegView.as_view(), name='CompanyReg'),
    path('logout', views.logout_view, name='logout'),    

    ]
