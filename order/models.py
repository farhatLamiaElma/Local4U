from django.db import models
from accounts.models import Customer, Farmer
from product.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    # Order related to a specific customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # For guest users who place an order without an account
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_address = models.TextField(null=True, blank=True)

    # Order status to track progress (e.g., Pending, Fulfilled)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Display order details based on customer or guest
        if self.customer:
            return f"Order by {self.customer.user.username} - {self.id}"
        return f"Guest Order by {self.guest_name} - {self.id}"

    # Calculate total price of the order based on order items
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    # Update order status based on the status of order items
    def update_status(self):
        items = self.items.all()
        if all(item.status == 'Delivered' for item in items):
            self.status = 'Delivered'
        elif all(item.status == 'Fulfilled' for item in items):
            self.status = 'Fulfilled'
        elif any(item.status in ['Shipped', 'Delivered'] for item in items):
            self.status = 'Partially Fulfilled'
        else:
            self.status = 'Pending'
        self.save()

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    # Link each order item to the specific order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price when the order is placed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Calculate the total price of a single order item based on quantity
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        # Display order item details
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Display cart details
        return f"{self.customer} - {self.product} - {self.quantity}"

    @property
    # Calculate total price of the cart item based on product price and quantity
    def total_price(self):
        return self.product.price * self.quantity

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('PayPal', 'PayPal'),
    ]

    # Link payment to a specific order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='PayPal')
    status = models.CharField(max_length=50, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Display payment status and associated order
        return f"Payment {self.id} - {self.order} - {self.status}"
