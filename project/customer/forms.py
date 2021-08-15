from django import forms
from .models import CustomerModel

class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = CustomerModel 
        fields = ("name","contact","phone",)
