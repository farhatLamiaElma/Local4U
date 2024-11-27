from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm, ProfileUpdateForm
from .models import CustomUser, Farmer, Customer, Admin, Notification
from product.models import Category, Product
from order.models import Order
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

def logout_view(request):
    logout(request)
    return redirect('home')

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

@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')
    return render(request, 'customer_dashboard.html', {'orders': orders})

def admin_dashboard(request):
    # Logic for the admin dashboard
    return render(request, 'admin_dashboard.html')

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            # Determine the redirect URL based on user role
            if hasattr(user, 'farmer'):
                return redirect('farmer_dashboard')
            elif hasattr(user, 'customer'):
                return redirect('customer_dashboard')
            else:
                return redirect('admin_dashboard')
            return redirect('update_profile')  # Redirect to the profile page
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was updated successfully!')
            # Determine the redirect URL based on user role
            if hasattr(user, 'farmer'):
                return redirect('farmer_dashboard')
            elif hasattr(user, 'customer'):
                return redirect('customer_dashboard')
            else:
                return redirect('admin_dashboard')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def notifications(request):
    # Fetch unread notifications for the logged-in user
    notifications = request.user.notifications.all()

    # Determine the dashboard URL
    if hasattr(request.user, 'farmer'):
        dashboard_url = 'farmer_dashboard'
    elif hasattr(request.user, 'customer'):
        dashboard_url = 'customer_dashboard'
    else:
        dashboard_url = 'admin_dashboard'  # Default for admins or other roles

    # Mark notifications as read
    notifications.update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'dashboard_url': dashboard_url
    })


