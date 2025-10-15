# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """Форма оформления заказа"""
    class Meta:
        model = Order
        fields = ["name", "email", "phone", "address"]
