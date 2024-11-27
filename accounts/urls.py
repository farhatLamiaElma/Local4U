from django.urls import path
from . import views
from .views import register, login_view, farmer_dashboard

urlpatterns = [
    # Registration page URL, handling user sign-up
    path('register/', views.register, name='register'),

    # Login page accessed via the registration process or directly
    path('register/login/', views.login_view, name='login'),

    # Login page URL for user authentication
    path('login/', views.login_view, name='login'),

    # Logout URL, logging the user out and redirecting to home
    path('logout/', views.logout_view, name='logout'),

    # Profile update page where users can edit their personal information
    path('profile/update/', views.update_profile, name='update_profile'),

    # Password change page where users can modify their password
    path('profile/change-password/', views.change_password, name='change_password'),

    # Farmer dashboard URL for managing products and categories
    path('farmer/dashboard/', farmer_dashboard, name='farmer_dashboard'),

    # Customer dashboard displaying orders for the logged-in customer
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Admin dashboard for admin-level management
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Notifications page showing unread notifications for the user
    path('notifications/', views.notifications, name='notifications'),
]
