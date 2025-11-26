from django.contrib import admin
from company.models import Company, CompanyMembership, Company_Model


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'city', 'state_province', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'state_province']
    search_fields = ['name', 'email', 'city', 'owner__username']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'email', 'phone', 'owner')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state_province', 'postal_code', 'country')
        }),
        ('Business Details', {
            'fields': ('license_number', 'tax_id')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__username', 'user__email', 'company__name']
    raw_id_fields = ['user', 'company']


# Legacy model
@admin.register(Company_Model)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'company_name', 'city', 'company_email']

