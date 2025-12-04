from django import forms
from products.models import (
    ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct, BreederType, InventoryCategory, DiseaseCaseStatus, ChickStatus
)

# --- Batch & Health -------------------------------------------------------
class ChickBatchForm(forms.ModelForm):
    class Meta:
        model = ChickBatch
        fields = ['breeder_type', 'hatch_date', 'initial_count', 'current_count', 'farm_location', 'source', 'status', 'notes']
        widgets = {
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'hatch_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'initial_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class HealthCheckForm(forms.ModelForm):
    class Meta:
        model = HealthCheck
        fields = ['check_date', 'diseased_count', 'mortality_count', 'average_weight_g', 'notes']
        widgets = {
            'check_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diseased_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'mortality_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_weight_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# --- Feed -----------------------------------------------------------------
class FeedFormulaForm(forms.ModelForm):
    class Meta:
        model = FeedFormula
        fields = ['name', 'breeder_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class FeedScheduleForm(forms.ModelForm):
    class Meta:
        model = FeedSchedule
        fields = ['formula', 'date', 'quantity_kg']
        widgets = {
            'formula': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# --- Medicine & Treatment -------------------------------------------------
class MedicineProductForm(forms.ModelForm):
    class Meta:
        model = MedicineProduct
        fields = ['name', 'breeder_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class TreatmentRecordForm(forms.ModelForm):
    class Meta:
        model = TreatmentRecord
        fields = ['medicine', 'date_administered', 'dosage', 'administered_by', 'purpose', 'notes']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'date_administered': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'administered_by': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# --- Disease --------------------------------------------------------------
class DiseaseCatalogForm(forms.ModelForm):
    class Meta:
        model = DiseaseCatalog
        fields = ['name', 'breeder_type', 'severity', 'mortality_rate',
                 'symptoms', 'treatment', 'prevention', 'description']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 4}),
            'treatment': forms.Textarea(attrs={'rows': 4}),
            'prevention': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DiseaseCaseForm(forms.ModelForm):
    class Meta:
        model = DiseaseCase
        fields = ['disease', 'date_detected', 'affected_count', 'status', 'notes']
        widgets = {
            'disease': forms.Select(attrs={'class': 'form-select'}),
            'date_detected': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'affected_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# --- Inventory ----------------------------------------------------
class InventoryProductForm(forms.ModelForm):
    class Meta:
        model = InventoryProduct
        fields = ['sku', 'name', 'category', 'breeder_type', 'unit', 'stock_on_hand', 'reorder_point', 'cost_price', 'sale_price', 'is_active']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_on_hand': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_point': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---------------------------------------------------------------------------
# NOTE: Removed forms for deleted models (Stock, Vendor, PurchaseOrder, RFID)
# ---------------------------------------------------------------------------

