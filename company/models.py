from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Company(models.Model):
    """
    Central organization model - each company manages its own poultry operations
    """
    name = models.CharField(max_length=200, unique=True, help_text="Company/Farm name")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly company identifier")

    # Contact Information
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="USA")

    # Business Details
    license_number = models.CharField(max_length=100, blank=True, help_text="Business/Farm license number")
    tax_id = models.CharField(max_length=50, blank=True, help_text="Tax ID/EIN")

    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Owner (the user who registered the company)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owned_companies')

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class CompanyMembership(models.Model):
    """
    Links users to companies with roles/permissions
    """
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
        ('VIEWER', 'Viewer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_memberships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.role})"


# Keep legacy model for backward compatibility during migration
class Company_Model(models.Model):
    company_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_phone = models.IntegerField()

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'company_company_model'
