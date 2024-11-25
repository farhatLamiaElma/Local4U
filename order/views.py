
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from accounts.models import Customer
from django.http import JsonResponse
from django.utils import timezone
from .models import Order, OrderItem, Payment
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
import json
#CART = {}

def cart_summary(request):
    cart = request.session.get('cart', {})
    total = sum(
        float(item['price']) * item['quantity'] for item in cart.values()
    )
    return render(request, 'cart_summary.html', {'cart': cart, 'total': total})

def cart_add(request, product_id):
    if request.method == 'POST':
        product_id = str(request.POST.get('product_id'))  # Ensure consistent key type
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        # Retrieve product
        product = get_object_or_404(Product, id=product_id)

        # Initialize cart in session if not already done
        cart = request.session.get('cart', {})

        # Add or update product in the cart
        if product_id in cart:
            # Replace the quantity with the new one
            cart[product_id]['quantity'] = quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
            }

        # Save updated cart to session
        request.session['cart'] = cart

        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart_summary')
    return redirect('products_by_category')


def cart_remove(request, product_id):
    product_id = str(product_id)
    # Retrieve cart from session
    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart  # Save updated cart to session
        # Show success message
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    return redirect("cart_summary")

def cart_update(request, product_id):
    # Retrieve cart from session
    product_id = str(product_id)
    cart = request.session.get('cart', {})

    quantity = int(request.POST.get("quantity", 1))

    if product_id in cart:
        cart[product_id]["quantity"] = quantity
        messages.success(request, "Cart updated.")

        # Save the updated cart back to the session
        request.session['cart'] = cart
    else:
        messages.error(request, "Item not found in cart.")
    return redirect("cart_summary")



from django.utils import timezone

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect("cart_summary")

        # Create a new Order
        customer = request.user.customer  # Assuming the user is authenticated and linked to a Customer
        order = Order.objects.create(
            customer=customer,
            delivery_address=request.POST.get('delivery_address', customer.user.address),
            order_date=timezone.now(),
        )

        # Iterate through the cart and create OrderItems
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                farmer=product.farmer,  # Set the farmer based on the product
                quantity=quantity,
                price=product.price  # Price at the time of placing the order
            )

        # Clear the cart after placing the order
        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_summary", order_id=order.id)

    return redirect("cart_summary")


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, 'order_summary.html', {'order': order})




from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_summary')

    total_amount = sum(
        float(item['price']) * item['quantity'] for item in cart.values()
    )

    host = request.get_host()

    # Prepare PayPal payment details without the custom field
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f"{total_amount:.2f}",
        'item_name': "Cart Purchase",
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
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







from django.core.exceptions import ObjectDoesNotExist


from paypal.standard.models import ST_PP_COMPLETED



def payment_successful(request):
    payer_id = request.GET.get('PayerID')

    # Debugging logs
    print(f"PayerID: {payer_id}")

    # Retrieve cart from session
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "No cart data found.")
        return redirect('cart_summary')

    try:
        customer = request.user.customer
        total_amount = sum(
            float(item['price']) * item['quantity'] for item in cart.values()
        )

        # Create the Order
        order = Order.objects.create(
            customer=customer,
            delivery_address=request.GET.get('address', customer.user.address),
        )

        # Create OrderItems
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                farmer=product.farmer,
                quantity=item['quantity'],
                price=product.price,
            )

        # Create Payment
        Payment.objects.create(
            order=order,
            amount=total_amount,
            payment_method="PayPal",
            status="Completed",
        )

        # Clear the cart
        request.session['cart'] = {}
        return render(request, 'payment_successful.html', {'order': order})

    except Exception as e:
        print(f"Error in payment_successful: {e}")
        messages.error(request, "An error occurred while processing your payment.")
        return redirect('payment-failed')




def payment_failed(request):
    return render(request, 'payment_failed.html')

from django.contrib.auth.decorators import login_required

@login_required
def farmer_orders(request):
    farmer = request.user.farmer  # Assuming the user is logged in as a farmer
    order_items = OrderItem.objects.filter(farmer=farmer).select_related('order', 'product')
    return render(request, 'farmer_orders.html', {'order_items': order_items})


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