from django.urls import path
from . import views

urlpatterns = [
    # All products
    path('all_products/', views.all_products, name='all_products'),
    # Product search
    path('search/', views.search_products, name='search_products'),
    # List of categories
    path('categories/', views.list_categories, name='list_categories'),
    # Products by category
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    # OR
    path('category/<str:category_name>/', views.products_by_category, name='products_by_category'),
    # List of farmers
    path('farmers/', views.list_farmers, name='list_farmers'),
    # Products by farmer
    path('farmer/<int:farmer_id>/', views.products_by_farmer, name='products_by_farmer'),
    # Discounted products
    path('discounted-products/', views.all_discounted_products, name='all_discounted_products'),
    # Product detail customer
    path('<int:product_id>/detail', views.product_detail, name='product_detail'),
    # Product detail farmer
    path('farmer/product/<int:product_id>/detail/', views.product_detail_farmer, name='product_detail_farmer'),
    # Add product by farmer
    path('add_product/', views.add_product, name='add_product'),
    # Update product price
    path('update_product_price/<int:product_id>/', views.update_product_price, name='update_product_price'),
    # Update product image
    path('update_product_image/<int:product_id>/', views.update_product_image, name='update_product_image'),
    # Update product quantity
    path('update_product_quantity/<int:product_id>/', views.update_product_quantity, name='update_product_quantity'),
    # View sales by farmer
    path('view_sales/<int:product_id>/', views.view_sales, name='view_sales'),
    # Create sale
    path('sale/create/', views.create_seasonal_sale, name='create_seasonal_sale'),
    # Seasonal sales
    path('seasonal-sales/', views.list_seasonal_sales, name='list_seasonal_sales'),
    # Remove sale
    path('remove-sale/<int:sale_id>/', views.remove_seasonal_sale_discount, name='remove_seasonal_sale_discount'),

]
