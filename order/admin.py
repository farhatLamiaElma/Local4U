from django.contrib import admin
from .models import Order, Cart, Payment, OrderItem
# from .models import Coupon
# Register your models here.

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(OrderItem)

