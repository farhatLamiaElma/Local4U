from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('delivery-info/', views.delivery_info, name='delivery_info'),
    path('FAQ/<int:farmer_id>/', views.FAQ, name='FAQ'),
    path('contact/', views.contact, name='contact'),

]