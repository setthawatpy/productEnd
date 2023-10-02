from django import forms
from general.models import *


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('__all__')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 60}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'minlength': '10', 'maxlength': '10'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
