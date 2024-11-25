from django.db import models
from accounts.models import Farmer
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    def __str__(self):
        return self.name


# Model for Discount Codes
class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Unique code for the discount
    discount_percentage = models.FloatField()  # Discount percentage (e.g., 10 for 10%)
    active = models.BooleanField(default=True)  # Whether the discount is active
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # The farmer who created the discount
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Expiry date for the discount code

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

# Model for Seasonal Sales
class SeasonalSale(models.Model):
    name = models.CharField(max_length=100)  # Name of the sale event
    discount_percentage = models.FloatField()  # Discount percentage for the sale
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Optional: Specific category
    products = models.ManyToManyField(Product, blank=True)  # Optional: Specific products
    start_date = models.DateTimeField()  # Start date of the sale
    end_date = models.DateTimeField()  # End date of the sale
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # The farmer who created the sale

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"
