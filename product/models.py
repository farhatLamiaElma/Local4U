from django.db import models
from accounts.models import Farmer, Customer
from django.conf import settings
from decimal import Decimal


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
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    @property
    def discount_percentage(self):
        if self.discounted_price:
            return int(((self.price - self.discounted_price) / self.price) * 100)
        return None

    def get_display_price(self):
        """Get the price to display (discounted if available)."""
        return self.discounted_price if self.discounted_price else self.price

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.product.name}"

class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.farmer.user.username} to Review {self.review.id}"


# Model for Seasonal Sales
class SeasonalSale(models.Model):
    name = models.CharField(max_length=100)  # Name of the sale event
    discount_percentage = models.FloatField()  # Discount percentage for the sale
    products = models.ManyToManyField(Product, blank=True)  # Optional: Specific products
    start_date = models.DateTimeField()  # Start date of the sale
    end_date = models.DateTimeField()  # End date of the sale
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # The farmer who created the sale

    def apply_discount(self):
        """Apply the discount to the products."""
        print("Applying discount...")
        discount_factor = Decimal(1 - self.discount_percentage / 100)  # Convert to Decimal
        for product in self.products.all():
            product.discounted_price = product.price * discount_factor
            product.save()

    def remove_discount(self):
        """Remove the discount from the products."""
        for product in self.products.all():
            product.discounted_price = None
            product.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the sale instance
        self.apply_discount()  # Apply the discount to associated products

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"
