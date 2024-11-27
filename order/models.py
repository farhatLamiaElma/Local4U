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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # For guest users
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_address = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    #delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.customer:
            return f"Order by {self.customer.user.username} - {self.id}"
        return f"Guest Order by {self.guest_name} - {self.id}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())  # Sum total prices of all order items

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.product} - {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('PayPal', 'PayPal'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='PayPal')
    status = models.CharField(max_length=50, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.order} - {self.status}"


