from django.contrib import admin
from .models import Product, Category, Review, ReviewReply
# from .models import Coupon
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewReply)
# admin.site.register(Coupon)