from http.client import HTTPResponse

from django.shortcuts import render, redirect, get_object_or_404

from home.models import FAQs
from product.models import Category
from accounts.models import Farmer

def home(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()
    return render(request, 'home.html', {'categories': categories, 'farmers': farmers})

def about_us(request):
    return render(request, 'about_us.html')

def FAQ(request,farmer_id):

    farmers = Farmer.objects.all()
    faqs = FAQs.objects.filter(farmer_id=farmer_id)
    farmer = farmers.first() if farmers.exists() else None
    return render(request, 'FAQ.html', {'farmer': farmer, 'faqs': faqs, 'farmers': farmers})

