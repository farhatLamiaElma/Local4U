from django.urls import path
from . import views

urlpatterns = [
    # Product search
    path('search/', views.search_products, name='search_products'),
    # Products by category
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    # OR
    path('category/<str:category_name>/', views.products_by_category, name='products_by_category'),
    # Add the farmer filtering URL if it's not already there:
    path('farmer/<int:farmer_id>/', views.products_by_farmer, name='products_by_farmer'),
]
