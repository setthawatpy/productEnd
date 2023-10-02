from django import forms
from contract.models import *

class ContractForm(forms.ModelForm):  
    class Meta:
        model = Contract
        fields = ['customer', 'period', 'interest_rate', 'picture']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'weight', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['picture', 'status']
        widgets = {
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }
        