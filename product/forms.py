from django import forms
from .models import Product, Review, ReviewReply, SeasonalSale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image']  # Add 'image' if applicable

class ProductPriceUpdateForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="New Price")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...'}),
        }
        labels = {
            'review_text': 'Your Review',
        }

class ReviewReplyForm(forms.ModelForm):
    class Meta:
        model = ReviewReply
        fields = ['reply_text']
        widgets = {
            'reply_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'reply_text': 'Reply to Review',
        }


# Form for Seasonal Sales
class SeasonalSaleForm(forms.ModelForm):
    class Meta:
        model = SeasonalSale
        fields = ['name', 'discount_percentage', 'products', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop('farmer', None)  # Pass farmer instance to filter products
        super().__init__(*args, **kwargs)
        if farmer:
            self.fields['products'].queryset = Product.objects.filter(farmer=farmer)
