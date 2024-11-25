from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Order, OrderItem, Payment
from product.models import Product
from accounts.models import Customer
import json
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    print(f"IPN Received: {ipn}")
    print(f"Payment Status: {ipn.payment_status}")

    if ipn.payment_status == ST_PP_COMPLETED:
        print("Payment Completed")
        try:
            customer = Customer.objects.get(user__email=ipn.payer_email)
        except Customer.DoesNotExist:
            return

        # Create the Order
        order = Order.objects.create(
            customer=customer,
            delivery_address=ipn.address_street,
        )

        # Extract cart data from custom field
        cart = json.loads(ipn.custom)  # Convert string back to dictionary
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                farmer=product.farmer,
                quantity=item['quantity'],
                price=product.price,
            )

        # Record the payment
        Payment.objects.create(
            order=order,
            amount=ipn.mc_gross,
            payment_method="PayPal",
            status="Completed",
        )
