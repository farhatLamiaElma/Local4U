from http.client import HTTPResponse

from django.shortcuts import render,  redirect
from product.models import Category
from accounts.models import Farmer

def home(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()
    return render(request, 'home.html', {'categories': categories, 'farmers': farmers})

def about_us(request):
    return render(request, 'about_us.html')

