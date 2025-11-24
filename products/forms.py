from django import forms
from products.models import *


class Chick_Form(forms.ModelForm):
    class Meta :
        model = Chick_Model
        fields = ['breeder_type', 'number_of_diseased_chicks', 'chicks_age']
        widgets = {
        'breeder': forms.Select(attrs={'class':'form-control'}),               
        'number_of_diseased_chicks': forms.NumberInput(attrs={'class':'form-control'}),
        'chicks_age': forms.NumberInput(attrs={'class':'form-control'}),
        }



class Medicine_Form(forms.ModelForm):
    class Meta :
        model = Medicine_Model
        fields = ['medicine_name', 'medicine_for_type_breed', 'description']
        widgets = {
        'medicine_name': forms.TextInput(attrs={'class':'form-control'}),
        'medicine_for_type_breed': forms.Select(attrs={'class':'form-control'}),
        'description': forms.TextInput(attrs={'class':'form-control'}),
        }


class Disease_Form(forms.ModelForm):
    class Meta :
        model = Disease_Model
        fields = ['disease_name', 'disease_in_type_of_breed', 'description']
        widgets = {
        'disease_name': forms.TextInput(attrs={'class':'form-control'}),
        'disease_in_type_of_breed': forms.Select(attrs={'class':'form-control'}),
        'description': forms.TextInput(attrs={'class':'form-control'}),
        }

class Feed_Form(forms.ModelForm):
    class Meta :
        model = Feed_Model
        fields = ['feed_name', 'feed_type', 'description']
        widgets = {
        'feed_name': forms.TextInput(attrs={'class':'form-control'}),
        'feed_type': forms.Select(attrs={'class':'form-control'}),
        'description': forms.TextInput(attrs={'class':'form-control'}),
        }