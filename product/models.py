from django.db import models
from accounts.models import Farmer, Customer
from django.conf import settings
from decimal import Decimal

# Model to represent product categories
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Optional category image

    def __str__(self):
        return self.name  # Display category name in admin panel and queries

# Model to represent products listed by farmers
class Product(models.Model):
    name = models.CharField(max_length=200)  # Name of the product
    description = models.TextField()  # Detailed description of the product
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category to which the product belongs
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Original price of the product
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discounted price if applicable
    stock = models.PositiveIntegerField()  # Available stock quantity
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # Farmer who owns the product
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the product was last updated
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Optional product image

    @property
    def discount_percentage(self):
        """Calculate the discount percentage."""
        if self.discounted_price:
            return int(((self.price - self.discounted_price) / self.price) * 100)  # Discount formula
        return None

    def get_display_price(self):
        """Get the price to display (discounted if available)."""
        return self.discounted_price if self.discounted_price else self.price

    def __str__(self):
        return self.name  # Display product name in admin panel and queries

# Model for product reviews by customers
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # Associated product
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Customer who wrote the review
    review_text = models.TextField()  # Content of the review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created

    def __str__(self):
        return f"Review by {self.customer.username} for {self.product.name}"

# Model for farmers to reply to customer reviews
class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')  # Associated review
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # Farmer who replied
    reply_text = models.TextField()  # Content of the reply
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the reply was created

    def __str__(self):
        return f"Reply by {self.farmer.user.username} to Review {self.review.id}"

# Model for seasonal sales created by farmers
class SeasonalSale(models.Model):
    name = models.CharField(max_length=100)  # Name of the seasonal sale event
    discount_percentage = models.FloatField()  # Discount percentage for the sale
    products = models.ManyToManyField(Product, blank=True)  # Products associated with the sale (optional)
    start_date = models.DateTimeField()  # Start date and time of the sale
    end_date = models.DateTimeField()  # End date and time of the sale
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # Farmer who created the sale

    def apply_discount(self):
        """Apply the discount to the associated products."""
        discount_factor = Decimal(1 - self.discount_percentage / 100)  # Calculate the discount factor
        for product in self.products.all():
            product.discounted_price = product.price * discount_factor  # Set the discounted price
            product.save()  # Save the updated product

    def remove_discount(self):
        """Remove the discount from the associated products."""
        for product in self.products.all():
            product.discounted_price = None  # Reset the discounted price
            product.save()  # Save the updated product

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the sale instance
        self.apply_discount()  # Automatically apply discounts upon saving the sale

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"  # Display sale name and discount percentage
