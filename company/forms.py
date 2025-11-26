from django import forms
from company.models import Company, CompanyMembership, Company_Model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class CompanyRegistrationForm(UserCreationForm):
    """
    Combined form for user registration and company creation
    """
    # User fields
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    # Company fields
    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm/Company Name'})
    )
    company_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'company@email.com'})
    )
    phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'})
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state_province = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Company.objects.filter(name__iexact=company_name).exists():
            raise ValidationError("A company with this name already exists.")
        return company_name

    def clean_company_email(self):
        company_email = self.cleaned_data.get('company_email')
        if Company.objects.filter(email=company_email).exists():
            raise ValidationError("This company email is already registered.")
        return company_email

    def save(self, commit=True):
        # Save the user
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

            # Create the company
            company = Company.objects.create(
                name=self.cleaned_data['company_name'],
                slug=slugify(self.cleaned_data['company_name']),
                email=self.cleaned_data['company_email'],
                phone=self.cleaned_data.get('phone', ''),
                city=self.cleaned_data['city'],
                state_province=self.cleaned_data['state_province'],
                owner=user,
                is_active=True
            )

            # Create owner membership
            CompanyMembership.objects.create(
                user=user,
                company=company,
                role='OWNER',
                is_active=True
            )

        return user


class CompanyProfileForm(forms.ModelForm):
    """
    Form for updating company profile details
    """
    class Meta:
        model = Company
        fields = [
            'name', 'email', 'phone', 'address_line1', 'address_line2',
            'city', 'state_province', 'postal_code', 'country',
            'license_number', 'tax_id'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apt, Suite, etc. (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state_province': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    """
    Custom login form for company users
    """
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': 'Password'})
    )


# Legacy form - kept for backward compatibility
class Company_Form(forms.ModelForm):
    class Meta:
        model = Company_Model
        fields = ['company_name', 'city', 'state_province', 'company_email', 'company_phone']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state_province': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Legacy aliases
CompanyRegForm = CompanyRegistrationForm
Login_Form = LoginForm

