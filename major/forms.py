from django import forms
from .models import *

class Breeder_Form(forms.ModelForm):
    class Meta :
        model = Breeder_Model
        fields = ['breeder_type', 'breeder_age']
        widgets = {
        'breeder_type': forms.TextInput(attrs={'class':'form-control'}),
        'breeder_age': forms.NumberInput(attrs={'class':'form-control'})
        
        }
class Distribution_Form(forms.ModelForm):
    class Meta :
        model = Distributed_among_companies
        fields = ['company_name', 'total_number_of_chicks', 'infacted_chicks', 'diseased_chicks',]
        widgets = {
        'company_name': forms.TextInput(attrs={'class':'form-control'}),
        'total_number_of_chicks': forms.NumberInput(attrs={'class':'form-control'}),
        'infacted_chicks': forms.NumberInput(attrs={'class':'form-control'}),
        'diseased_chicks': forms.NumberInput(attrs={'class':'form-control'}),
        # 'date_of_departure': forms.NumberInput(attrs={'class':'form-control'}),
        
        }


