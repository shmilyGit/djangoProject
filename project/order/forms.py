from django import forms
from .models import OrderModel 

class OrderAddForm(forms.ModelForm):
    class Meta:
        model = OrderModel 
        fields = ("orderid","customer","contact","phone","deposit",
                  "price", "comment", "orderdate")
