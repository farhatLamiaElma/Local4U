from django import forms

class GuestCheckoutForm(forms.Form):
    guest_name = forms.CharField(max_length=100, required=True, label="Name")
    guest_email = forms.EmailField(required=True, label="Email")
    guest_address = forms.CharField(widget=forms.Textarea, required=True, label="Address")
