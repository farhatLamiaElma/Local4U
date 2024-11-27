from django.urls import path
from . import views

urlpatterns = [
    # Home page URL, typically showing the main landing page of the site
    path('', views.home, name='home'),

    # About Us page URL, providing information about the website or company
    path('aboutus/', views.about_us, name='aboutus'),

    # Delivery information page URL, detailing shipping and delivery policies
    path('delivery-info/', views.delivery_info, name='delivery_info'),

    # FAQ page for a specific farmer, identified by the farmer's ID
    path('FAQ/<int:farmer_id>/', views.FAQ, name='FAQ'),

    # Contact page URL, typically for users to get in touch with the company
    path('contact/', views.contact, name='contact'),
]
