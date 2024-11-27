from django.urls import path
from . import views
from .views import register, login_view, farmer_dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('farmer/dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/', views.notifications, name='notifications'),
]

