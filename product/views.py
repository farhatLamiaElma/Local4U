from django.shortcuts import render, get_object_or_404,redirect
from accounts.models import Farmer
from .models import Product, Category
from .forms import ProductForm
from django.contrib import messages
from order.models import Order
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user.farmer  # Assign the logged-in farmer as the product owner
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def update_product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.image = request.FILES.get('image')
        product.save()
        messages.success(request, 'Image updated successfully!')
        return redirect('farmer_dashboard')

    return render(request, 'update_product_image.html', {'product': product})




def update_product_price(request, product_id):
    # Retrieve the product by ID
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get the new price from the form data
        new_price = request.POST.get('price')

        try:
            new_price = float(new_price)
            if new_price <= 0:
                raise ValueError("Price must be positive.")  # Ensure price is positive

            # Update the product's price
            product.price = new_price
            product.save()

            # Display a success message
            messages.success(request, f"Price for {product.name} updated successfully!")
            return redirect('farmer_dashboard')  # Redirect to the farmer dashboard

        except (ValueError, TypeError):
            # Handle invalid price input
            messages.error(request, "Please enter a valid price.")

    return render(request, 'update_product_price.html', {'product': product})
def update_product_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity'))
            if new_quantity < 0:
                raise ValueError
            product.stock = new_quantity
            product.save()
            messages.success(request, 'Quantity updated successfully!')
            return redirect('farmer_dashboard')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity. Please enter a valid number.')
    return render(request, 'update_product_quantity.html', {'product': product})

@login_required
def view_sales(request, product_id):
    # Get the product and ensure it belongs to the logged-in farmer
    product = get_object_or_404(Product, id=product_id, farmer=request.user.farmer)

    # Retrieve orders associated with this product
    orders = Order.objects.filter(product=product)
    total_sales = sum(order.total_price() for order in orders)

    # Render the sales page
    return render(request, 'view_sales.html', {
        'product': product,
        'orders': orders,
        'total_sales': total_sales
    })
