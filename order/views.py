from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from accounts.models import Customer
from django.http import JsonResponse
from .models import Order, OrderItem, Payment
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
import uuid
from django.urls import reverse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from paypal.standard.models import ST_PP_COMPLETED

# Handles displaying the cart summary, including total price
def cart_summary(request):
    cart = request.session.get('cart', {})
    total = sum(
        float(item['price']) * int(item['quantity']) for item in cart.values()
    )
    return render(request, 'cart_summary.html', {'cart': cart, 'total': total})

# Adds a product to the cart or updates its quantity
def cart_add(request, product_id):
    if request.method == 'POST':
        product_id = str(request.POST.get('product_id'))  # Ensure product ID consistency as a string
        quantity = int(request.POST.get('quantity', 1))  # Default quantity to 1 if not specified

        # Fetch product details or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # Use the discounted price if available, otherwise use the regular price
        price = product.discounted_price if product.discounted_price else product.price

        # Initialize the cart in the session if it doesn't exist
        cart = request.session.get('cart', {})

        # Update the product's quantity if it already exists in the cart
        if product_id in cart:
            cart[product_id]['quantity'] = quantity
        else:
            # Add new product to the cart
            cart[product_id] = {
                'name': product.name,
                'price': str(price),
                'original_price': str(product.price),
                'quantity': quantity,
            }

        # Save the updated cart back to the session
        request.session['cart'] = cart

        # Inform the user that the product has been added
        messages.success(request, f"{product.name} added to cart!")
        referer_url = request.META.get('HTTP_REFERER', None)
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('products_by_category')
    return redirect('products_by_category')

# Removes a product from the cart
def cart_remove(request, product_id):
    product_id = str(product_id)
    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart  # Save updated cart
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    return redirect("cart_summary")

# Updates the quantity of a product in the cart
def cart_update(request, product_id):
    product_id = str(product_id)
    cart = request.session.get('cart', {})

    quantity = int(request.POST.get("quantity", 1))  # Default quantity to 1

    if product_id in cart:
        cart[product_id]["quantity"] = quantity
        messages.success(request, "Cart updated.")
        request.session['cart'] = cart  # Save updated cart
    else:
        messages.error(request, "Item not found in cart.")
    return redirect("cart_summary")

# Places an order based on the current cart contents
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect("cart_summary")

        # Create a new order for the logged-in customer
        customer = request.user.customer
        order = Order.objects.create(
            customer=customer,
            delivery_address=request.POST.get('delivery_address', customer.user.address),
            order_date=timezone.now(),
        )

        # Create an OrderItem for each cart item
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                farmer=product.farmer,
                quantity=quantity,
                price=product.price,
            )

        # Clear the cart after placing the order
        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_summary", order_id=order.id)

    return redirect("cart_summary")

# Displays the details of a specific order
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, 'order_summary.html', {'order': order})

# Prepares the cart for checkout with PayPal
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_summary')

    total_amount = sum(
        float(item['price']) * item['quantity'] for item in cart.values()
    )

    host = request.get_host()

    # Set up PayPal payment details
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f"{total_amount:.2f}",
        'item_name': "Cart Purchase",
        'invoice': str(uuid.uuid4()),
        'currency_code': 'CAD',
        'notify_url': f"http://{host}/paypal/ipn/",
        'return_url': f"http://{host}/order/payment-successful/",
        'cancel_url': f"http://{host}/order/payment-failed/",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment,
        'total_amount': total_amount,
    }
    return render(request, 'checkout.html', context)

# Handles successful payments
def payment_successful(request):
    payer_id = request.GET.get('PayerID')
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "No cart data found.")
        return redirect('cart_summary')

    try:
        customer = request.user.customer
        total_amount = sum(
            float(item['price']) * item['quantity'] for item in cart.values()
        )

        order = Order.objects.create(
            customer=customer,
            delivery_address=request.GET.get('address', customer.user.address),
        )

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                farmer=product.farmer,
                quantity=item['quantity'],
                price=product.price,
            )

        Payment.objects.create(
            order=order,
            amount=total_amount,
            payment_method="PayPal",
            status="Completed",
        )

        request.session['cart'] = {}
        return render(request, 'payment_successful.html', {'order': order})

    except Exception as e:
        messages.error(request, "An error occurred while processing your payment.")
        return redirect('payment-failed')

# Handles payment failures
def payment_failed(request):
    return render(request, 'payment_failed.html')

# Displays orders related to the logged-in farmer
@login_required
def farmer_orders(request):
    farmer = request.user.farmer
    order_items = OrderItem.objects.filter(farmer=farmer).select_related('order', 'product')
    return render(request, 'farmer_orders.html', {'order_items': order_items})

# Updates the status of an order item by the farmer
@login_required
def update_order_item_status(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, farmer=request.user.farmer)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Shipped', 'Delivered']:
            order_item.status = new_status
            order_item.save()
            order_item.order.update_status()
            messages.success(request, f"Order item status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status.")

    return redirect('farmer_orders')
