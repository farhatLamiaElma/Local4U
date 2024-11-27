from django.shortcuts import render, get_object_or_404,redirect
from accounts.models import Farmer, Notification
from .models import Product, Category, Review, ReviewReply, SeasonalSale
from .forms import ProductForm, ReviewForm, ReviewReplyForm, SeasonalSaleForm
from django.contrib import messages
from order.models import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# View to display all products with pagination
def all_products(request):
    products_list = Product.objects.all()  # Retrieve all products
    paginator = Paginator(products_list, 20)  # Display 20 products per page
    page_number = request.GET.get('page')  # Get the current page number from request
    products = paginator.get_page(page_number)  # Fetch products for the requested page

    return render(request, 'all_products.html', {'products': products})

# View to search for products by name or farmer's location
def search_products(request):
    query = request.GET.get('q')  # Retrieve the search query from URL parameters
    products = Product.objects.all()  # Start with all products

    if query:
        # Filter products by name or farmer's location
        products = products.filter(
            Q(name__icontains=query) |  # Filter by product name
            Q(farmer__user__address__icontains=query)  # Filter by farmer's address
        )

    return render(request, 'search_products.html', {
        'products': products,
        'query': query
    })

# View to display products belonging to a specific category
def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Get the category by ID or return 404
    products = Product.objects.filter(category=category)  # Get products of this category
    return render(request, 'products_by_category.html', {'products': products, 'category': category})

# View to display products added by a specific farmer
def products_by_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)  # Get the farmer by ID or return 404
    products = Product.objects.filter(farmer=farmer)  # Get products owned by the farmer
    return render(request, 'products_by_farmer.html', {'products': products, 'farmer': farmer})

# View to display all discounted products
def all_discounted_products(request):
    discounted_products = Product.objects.filter(discounted_price__isnull=False).order_by('-updated_at')  # Filter products with discounts
    paginator = Paginator(discounted_products, 20)  # Paginate discounted products
    page_number = request.GET.get('page')  # Get current page number
    products_page = paginator.get_page(page_number)  # Fetch products for the requested page
    return render(request, 'discounted_products.html', {'products': products_page})

# View to display the details of a specific product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve product or return 404
    reviews = product.reviews.all()  # Fetch all reviews related to the product

    if request.method == 'POST':  # Handle review submission
        if request.user.is_authenticated and hasattr(request.user, 'customer'):  # Check if user is a customer
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product  # Associate review with the product
                review.customer = request.user  # Associate review with the customer
                review.save()

                # Notify the farmer about the review
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

# View for farmers to view product details and manage reviews
@login_required
def product_detail_farmer(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user.farmer)  # Ensure farmer owns the product
    reviews = product.reviews.all()  # Get all reviews for the product

    if request.method == 'POST':
        if 'reply' in request.POST:  # Handle reply to a review
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            form = ReviewReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.review = review  # Associate reply with the review
                reply.farmer = request.user.farmer  # Associate reply with the farmer
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

# View to add a new product by a farmer
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user.farmer  # Assign logged-in farmer as product owner
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

# View to update the image of an existing product
def update_product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve product or return 404
    if request.method == 'POST':
        product.image = request.FILES.get('image')  # Update product image
        product.save()
        messages.success(request, 'Image updated successfully!')
        return redirect('farmer_dashboard')

    return render(request, 'update_product_image.html', {'product': product})

# View to update the price of a product
def update_product_price(request, product_id):
    # Retrieve the product by ID
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get the new price from the form data
        new_price = request.POST.get('price')

        try:
            new_price = float(new_price)  # Convert input to a float
            if new_price <= 0:
                raise ValueError("Price must be positive.")  # Ensure the price is valid

            # Update the product's price
            product.price = new_price
            product.save()

            # Display a success message
            messages.success(request, f"Price for {product.name} updated successfully!")
            return redirect('farmer_dashboard')  # Redirect to the farmer dashboard

        except (ValueError, TypeError):  # Handle invalid or non-numeric input
            messages.error(request, "Please enter a valid price.")

    return render(request, 'update_product_price.html', {'product': product})

# View to update the quantity (stock) of a product
def update_product_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity'))  # Convert input to an integer
            if new_quantity < 0:  # Ensure quantity is non-negative
                raise ValueError
            product.stock = new_quantity  # Update the stock
            product.save()
            messages.success(request, 'Quantity updated successfully!')
            return redirect('farmer_dashboard')
        except (ValueError, TypeError):  # Handle invalid or non-numeric input
            messages.error(request, 'Invalid quantity. Please enter a valid number.')
    return render(request, 'update_product_quantity.html', {'product': product})

# View for farmers to view sales details of a specific product
@login_required
def view_sales(request, product_id):
    # Retrieve the product and ensure it belongs to the logged-in farmer
    product = get_object_or_404(Product, id=product_id, farmer=request.user.farmer)

    # Retrieve all orders associated with this product
    orders = Order.objects.filter(product=product)
    total_sales = sum(order.total_price() for order in orders)  # Calculate total sales amount

    # Render the sales page
    return render(request, 'view_sales.html', {
        'product': product,
        'orders': orders,
        'total_sales': total_sales
    })

# View to create a new seasonal sale and apply discounts
@login_required
def create_seasonal_sale(request):
    if request.method == 'POST':
        form = SeasonalSaleForm(request.POST, farmer=request.user.farmer)  # Include farmer in the form
        if form.is_valid():
            sale = form.save(commit=False)
            sale.farmer = request.user.farmer  # Associate the sale with the logged-in farmer
            sale.save()
            form.save_m2m()  # Save many-to-many relationships
            sale.apply_discount()  # Apply the discount to associated products
            messages.success(request, 'Seasonal Sale created and discounts applied!')
            return redirect('list_seasonal_sales')
    else:
        form = SeasonalSaleForm(farmer=request.user.farmer)  # Initialize form with the farmer
    return render(request, 'create_seasonal_sale.html', {'sale_form': form})

# View to list all seasonal sales created by the logged-in farmer
@login_required
def list_seasonal_sales(request):
    farmer = request.user.farmer  # Get the logged-in farmer
    sales = SeasonalSale.objects.filter(farmer=farmer)  # Fetch all sales associated with the farmer
    return render(request, 'list_seasonal_sales.html', {'sales': sales})

# View to remove a seasonal sale and its associated discounts
@login_required
def remove_seasonal_sale_discount(request, sale_id):
    sale = get_object_or_404(SeasonalSale, id=sale_id, farmer=request.user.farmer)  # Ensure sale belongs to the farmer
    sale.remove_discount()  # Remove associated discounts
    sale.delete()  # Delete the seasonal sale
    messages.success(request, 'Seasonal Sale and discounts removed!')
    return redirect('list_seasonal_sales')

# View to list all farmers with pagination
def list_farmers(request):
    farmers = Farmer.objects.all()  # Retrieve all farmers
    paginator = Paginator(farmers, 10)  # Paginate farmers, 10 per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Fetch farmers for the current page

    return render(request, 'list_farmers.html', {'page_obj': page_obj})

# View to list all product categories with pagination
def list_categories(request):
    categories = Category.objects.all()  # Retrieve all categories
    paginator = Paginator(categories, 10)  # Paginate categories, 10 per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Fetch categories for the current page

    return render(request, 'list_categories.html', {'page_obj': page_obj})
