from django import forms
from company.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _


class Company_Form(forms.ModelForm):
    class Meta :
        model = Company_Model
        fields = ['company_name', 'city', 'state_province', 'company_email', 'company_phone']
        widgets = {
        'company_name': forms.TextInput(attrs={'class':'form-control'}),
        'city': forms.TextInput(attrs={'class':'form-control'}),
        'state_province': forms.TextInput(attrs={'class':'form-control'}),
        'company_email': forms.EmailInput(attrs={'class':'form-control'}),
        'company_phone': forms.NumberInput(attrs={'class':'form-control'}),
        
        }



class CompanyRegForm(UserCreationForm):  
    username = forms.CharField(label='Company Name' ,widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


        #     'username': forms.CharField(label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'username': forms.EmailField(label='Company Email', widget=forms.EmailInput( attrs={'class': 'form-control'})),
        #     'password1': forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'})),
        #     'username': forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'})),
        


# class CompanyRegForm(UserCreationForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

class Login_Form(AuthenticationForm):
    username = forms.CharField(label='Company Domain' ,widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    # company_Email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_('password'), strip=False, 
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

    class Meta :
        model = User
        fields = ['username', 'email', 'password']