from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.core.mail import send_mail
from django.contrib import messages
from .models import FAQs
from product.models import Category, Product, SeasonalSale
from accounts.models import Farmer

def home(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()
    products = Product.objects.all()[:10]
    discounted_products = Product.objects.filter(discounted_price__isnull=False).order_by('-updated_at')[:10]
    highest_discount = SeasonalSale.objects.aggregate(Max('discount_percentage'))['discount_percentage__max']
    return render(request, 'home.html',
        {'categories': categories,
                'farmers': farmers,
                'products': products,
                'discounted_products': discounted_products,
                'highest_discount': highest_discount,})

def about_us(request):
    return render(request, 'about_us.html')

def FAQ(request,farmer_id):

    farmers = Farmer.objects.all()
    faqs = FAQs.objects.filter(farmer_id=farmer_id)
    farmer = farmers.first() if farmers.exists() else None
    return render(request, 'FAQ.html', {'farmer': farmer, 'faqs': faqs, 'farmers': farmers})

def delivery_info(request):
    return render(request, 'delivery_info.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Combine name and message for better context
        full_message = f"Message from {name} ({email}):\n\n{message}"

        # Send the email
        send_mail(
            subject,
            full_message,
            'farhatlamia29@gmail.com',
            ['elmaf@uwindsor.ca'],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent. We'll get back to you shortly.")
        return render(request, 'contact.html')

    return render(request, 'contact.html')



