#from django.core.exceptions.ValidationError import messages
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from django.http import JsonResponse


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

