from django import forms
from product.models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }   


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'charge': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'picture1': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'picture1': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'picture2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'picture3': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'picture4': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'picture5': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }
