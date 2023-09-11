from django import forms
from contract.models import *

class ContractForm(forms.ModelForm):  
    class Meta:
        model = Contract
        fields = '__all__'  
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }


class ContractItemForm(forms.ModelForm):
    class Meta:
        model = ContractItem
        fields = '__all__'  
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }