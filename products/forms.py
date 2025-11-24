from django import forms
from django.forms import inlineformset_factory
from products.models import (
    ChickBatch, HealthCheck, FeedFormula, FeedSchedule,
    MedicineProduct, TreatmentRecord, DiseaseCatalog, DiseaseCase,
    InventoryProduct, StockMovement, Vendor, PurchaseOrder, PurchaseOrderItem,
    RFIDTag, MovementType, BreederType, InventoryCategory, PurchaseStatus, DiseaseCaseStatus
)

# --- Batch & Health -------------------------------------------------------
class ChickBatchForm(forms.ModelForm):
    class Meta:
        model = ChickBatch
        fields = ['breeder_type', 'hatch_date', 'initial_count', 'farm_location', 'source', 'notes']
        widgets = {
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'hatch_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'initial_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
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
        fields = ['name', 'breeder_type', 'severity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breeder_type': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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

# --- Inventory & Stock ----------------------------------------------------
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

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason', 'related_batch']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'related_batch': forms.Select(attrs={'class': 'form-select'}),
        }

# --- Vendors & Purchasing -------------------------------------------------
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_email', 'phone', 'is_active', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'order_date', 'expected_date', 'status', 'reference_code', 'notes']
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reference_code': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'unit_cost', 'received_quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'received_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    can_delete=True
)

# --- RFID -----------------------------------------------------------------
class RFIDTagForm(forms.ModelForm):
    class Meta:
        model = RFIDTag
        fields = ['tag_uid', 'is_active', 'assigned_batch']
        widgets = {
            'tag_uid': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_batch': forms.Select(attrs={'class': 'form-select'}),
        }