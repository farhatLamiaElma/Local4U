from django.shortcuts import render, get_object_or_404,redirect
from accounts.models import Farmer, Notification
from .models import Product, Category, Review, ReviewReply, SeasonalSale
from .forms import ProductForm, ReviewForm, ReviewReplyForm, SeasonalSaleForm
from django.contrib import messages
from order.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def all_products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 20)  # Show 10 products per page
    page_number = request.GET.get('page')  # Get the page number from the request
    products = paginator.get_page(page_number)  # Fetch the products for the current page

    return render(request, 'all_products.html', {'products': products})

# View to search for products by name
def search_products(request):
    query = request.GET.get('q')  # Retrieve the search query from the URL parameters
    products = Product.objects.all()  # Start with all products

    if query:
        # Filter products by name or by farmer's location
        products = products.filter(
            Q(name__icontains=query) |  # Search by product name
            Q(farmer__user__address__icontains=query)  # Search by farmer's location
        )

    return render(request, 'search_products.html', {
        'products': products,
        'query': query
    })
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

def all_discounted_products(request):
    discounted_products = Product.objects.filter(discounted_price__isnull=False).order_by('-updated_at')
    paginator = Paginator(discounted_products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    return render(request, 'discounted_products.html', {'products': products_page})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  # Fetch all reviews for the product

    if request.method == 'POST':
        if request.user.is_authenticated and hasattr(request.user, 'customer'):
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.customer = request.user
                review.save()

                # Notify the farmer about the new review
                message = f"{request.user.username} left a review on your product: {product.name}"
                Notification.objects.create(
                    recipient=product.farmer.user,
                    message=message
                )

                messages.success(request, "Your review has been submitted!")
                return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "Only customers can leave reviews.")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

@login_required
def product_detail_farmer(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user.farmer)
    reviews = product.reviews.all()

    if request.method == 'POST':
        if 'reply' in request.POST:  # Farmer replies to a review
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            form = ReviewReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.review = review
                reply.farmer = request.user.farmer
                reply.save()

                # Notify the customer about the reply
                message = f"{request.user.username} replied to your review on the product: {product.name}"
                Notification.objects.create(
                    recipient=review.customer,
                    message=message
                )

                messages.success(request, "Your reply has been added.")
                return redirect('product_detail_farmer', product_id=product_id)
        else:
            messages.error(request, "Invalid action.")
    else:
        form = ReviewReplyForm()

    return render(request, 'product_detail_farmer.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

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


@login_required
def create_seasonal_sale(request):
    if request.method == 'POST':
        form = SeasonalSaleForm(request.POST, farmer=request.user.farmer)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.farmer = request.user.farmer
            sale.save()
            form.save_m2m()  # Save the many-to-many relationship
            sale.apply_discount()
            messages.success(request, 'Seasonal Sale created and discounts applied!')
            return redirect('list_seasonal_sales')
    else:
        form = SeasonalSaleForm(farmer=request.user.farmer)
    return render(request, 'create_seasonal_sale.html', {'sale_form': form})

@login_required
def list_seasonal_sales(request):
    farmer = request.user.farmer  # Get the logged-in farmer
    sales = SeasonalSale.objects.filter(farmer=farmer)  # Get all seasonal sales for this farmer
    return render(request, 'list_seasonal_sales.html', {'sales': sales})

@login_required
def remove_seasonal_sale_discount(request, sale_id):
    sale = get_object_or_404(SeasonalSale, id=sale_id, farmer=request.user.farmer)
    sale.remove_discount()
    sale.delete()
    messages.success(request, 'Seasonal Sale and discounts removed!')
    return redirect('list_seasonal_sales')

def list_farmers(request):
    farmers = Farmer.objects.all()
    paginator = Paginator(farmers, 10)  # 10 farmers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_farmers.html', {'page_obj': page_obj})

def list_categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_categories.html', {'page_obj': page_obj})