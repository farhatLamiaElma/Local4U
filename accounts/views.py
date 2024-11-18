from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import CustomUser, Farmer, Customer, Admin
from product.models import Category, Product
from product.forms import ProductForm
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create entries in Farmer, Customer, or Admin table based on user type
            if user.user_type == 'farmer':
                Farmer.objects.create(user=user)
            elif user.user_type == 'customer':
                Customer.objects.create(user=user)
            elif user.user_type == 'admin':
                Admin.objects.create(user=user)

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            # Try to authenticate the user by username
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                # Try to authenticate the user by email if username authentication fails
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if user:
                login(request, user)
                # Redirect to the appropriate dashboard based on user type
                if user.user_type == 'farmer':
                    return redirect('farmer_dashboard')
                elif user.user_type == 'customer':
                    return redirect('customer_dashboard')
                elif user.user_type == 'admin':
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username, email, or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def farmer_dashboard(request):
    if not hasattr(request.user, 'farmer'):
        messages.error(request, 'You must be a farmer to access this page.')
        return redirect('login')

    categories = Category.objects.all()

    category_filter = request.GET.get('category')
    if category_filter:
        products = Product.objects.filter(category__name=category_filter, farmer=request.user.farmer)
    else:
        products = Product.objects.filter(farmer=request.user.farmer)

    print(f"Products for farmer {request.user.username}: {products}")  # Debugging line

    product_form = ProductForm(request.POST or None, request.FILES or None)
    if product_form.is_valid():
        new_product = product_form.save(commit=False)
        new_product.farmer = request.user.farmer
        new_product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('farmer_dashboard')

    return render(request, 'farmer_dashboard.html', {
        'categories': categories,
        'products': products,
        'product_form': product_form,
    })


def customer_dashboard(request):
    # Logic for the customer dashboard
    return render(request, 'customer_dashboard.html')

def admin_dashboard(request):
    # Logic for the admin dashboard
    return render(request, 'admin_dashboard.html')


from django.shortcuts import render, get_object_or_404
from product.models import Product  # Ensure the correct model is imported


def update_product_quantity(request, product_id):
    # Example logic for updating product quantity
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        new_quantity = request.POST.get("quantity")
        if new_quantity and new_quantity.isdigit():
            product.quantity = int(new_quantity)
            product.save()
            return render(request, 'success.html', {'message': 'Quantity updated successfully'})

    return render(request, 'update_quantity.html', {'product': product})