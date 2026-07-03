from django import forms
from .models import Item, SellRecord, UserProfile


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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "company_name",
            "business_email",
            "phone_number",
            "low_stock_threshold",
            "email_notifications",
            "auto_backup",
            "backup_frequency",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={
                "class": "form-control input-box",
                "placeholder": "Company Name",
            }),
            "business_email": forms.EmailInput(attrs={
                "class": "form-control input-box",
                "placeholder": "Business Email",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control input-box",
                "placeholder": "Phone Number",
            }),
            "low_stock_threshold": forms.NumberInput(attrs={
                "class": "form-control input-box",
                "min": 1,
            }),
            "email_notifications": forms.CheckboxInput(attrs={
                "class": "form-check-input check",
            }),
            "auto_backup": forms.CheckboxInput(attrs={
                "class": "form-check-input check",
            }),
            "backup_frequency": forms.Select(attrs={
                "class": "form-select select-box",
            }),
        }
        labels = {
            "business_email": "Business Email",
            "phone_number": "Phone Number",
            "low_stock_threshold": "Low stock threshold",
            "email_notifications": "Email notifications",
            "auto_backup": "Auto backup",
            "backup_frequency": "Backup frequency",
        }
