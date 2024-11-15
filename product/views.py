from django.shortcuts import render, get_object_or_404
from accounts.models import Farmer
from .models import Product, Category

# View to search for products by name
def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search_products.html', {'products': products, 'query': query})

# View to display products by category
def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products_by_category.html', {'products': products, 'category': category})

# View to display products by farmer
def products_by_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    products = Product.objects.filter(farmer=farmer)
    context = {
        'farmer': farmer,
        'products': products,
    }
    return render(request, 'products_by_farmer.html', {'products': products, 'farmer': farmer})

