from django.urls import path
from . import views
from .views import register, login_view, farmer_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('farmer/dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('update_quantity/<int:product_id>/', views.update_product_quantity, name='update_product_quantity'),
]

