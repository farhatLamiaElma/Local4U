from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image']  # Add 'image' if applicable

class ProductPriceUpdateForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="New Price")
