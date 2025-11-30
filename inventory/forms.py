from django import forms
from .models import Item, SellRecord


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "sku", "quantity", "unit_price", "category"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
            "sku": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "rows": 4,
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
            "category": forms.TextInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
        }


class SellRecordForm(forms.ModelForm):
    class Meta:
        model = SellRecord
        fields = ["quantity", "sell_price"]
        widgets = {
            "quantity": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
            "sell_price": forms.NumberInput(attrs={
                "class": "form-control form-control-sm bg-dark text-light border-secondary"
            }),
        }
