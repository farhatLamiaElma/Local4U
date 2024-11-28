from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User model that extends the default Django user model
class CustomUser(AbstractUser):
    # Defining user types for differentiation between farmers and customers
    USER_TYPES = (
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
    )
    # Full name field, can be left blank
    full_name = models.CharField(max_length=100, blank=True)
    # Address field
    address = models.CharField(max_length=255)
    # Contact number field
    contact_number = models.CharField(max_length=15)
    # User type (Farmer or Customer)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    # Profile picture with an upload path to 'static/profile_pictures/'
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)

    # String representation of the user, showing the username and user type
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


# Farmer model linked to CustomUser through a one-to-one relationship
class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # String representation, using the username of the associated user
    def __str__(self):
        return self.user.username


# Customer model linked to CustomUser through a one-to-one relationship
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # String representation, using the username of the associated user
    def __str__(self):
        return self.user.username


# Admin model linked to CustomUser through a one-to-one relationship
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # String representation, using the username of the associated user
    def __str__(self):
        return self.user.username


# Notification model to store messages sent to users
class Notification(models.Model):
    # Recipient of the notification, linked to the user model
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    # The notification message content
    message = models.TextField()
    # Date and time when the notification was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Boolean flag indicating whether the notification has been read
    is_read = models.BooleanField(default=False)

    # String representation showing the recipient and the start of the message
    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message[:20]}"
