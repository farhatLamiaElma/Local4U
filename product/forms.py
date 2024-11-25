from django import forms
from .models import Product, DiscountCode, SeasonalSale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image']  # Add 'image' if applicable

class ProductPriceUpdateForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="New Price")


# Form for Discount Codes
class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percentage', 'expires_at']

# Form for Seasonal Sales
class SeasonalSaleForm(forms.ModelForm):
    class Meta:
        model = SeasonalSale
        fields = ['name', 'discount_percentage', 'category', 'products', 'start_date', 'end_date']
