from django import forms
from purchase.models import *


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['gold_type', 'quantity', 'weight', 'price', 'id_card', 'first_name', 'last_name', 'address', 'phone_number', 'picture']
        widgets = {
            'gold_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_card': forms.TextInput(attrs={'class': 'form-control', 'minlength': 13, 'maxlength': 13}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 60}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'minlength': 10, 'maxlength': 10}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
