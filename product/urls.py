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
    path('add_product/', views.add_product, name='add_product'),
    path('update_product_price/<int:product_id>/', views.update_product_price, name='update_product_price'),
    path('update_product_image/<int:product_id>/', views.update_product_image, name='update_product_image'),
    path('update_product_quantity/<int:product_id>/', views.update_product_quantity, name='update_product_quantity'),
    path('view_sales/<int:product_id>/', views.view_sales, name='view_sales'),
]
