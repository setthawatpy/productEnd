from django import forms
from account.models import *


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('__all__')
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'minlength': 13, 'maxlength': 13}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 60}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'minlength': 10, 'maxlength': 10}),
            'profile1': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'profile2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }
    
    
class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('__all__')
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'minlength': 13, 'maxlength': 13}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 60}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'minlength': 10, 'maxlength': 10}),
            'profile1': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
            'profile2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*, video/*'}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='รหัสผ่านเดิม', widget=forms.PasswordInput)
    new_password = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='ยืนยันรหัสผ่านใหม่', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('รหัสผ่านใหม่และยืนยันรหัสผ่านไม่ตรงกัน')

    def save(self, user):
        new_password = self.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()
        
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='ยืนยันรหัสผ่านใหม่',widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('รหัสผ่านใหม่และยืนยันรหัสผ่านไม่ตรงกัน')

    def save(self, user):
        new_password = self.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()