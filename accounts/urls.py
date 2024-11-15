from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
