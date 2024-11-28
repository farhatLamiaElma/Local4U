from django.urls import path, include
from . import views

urlpatterns = [
    # Cart summary page URL, displaying current items in the user's cart
    path('', views.cart_summary, name='cart_summary'),

    # URL for adding a product to the cart by its ID
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),

    # URL for removing a specific product from the cart by its ID
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # URL for updating the quantity of a product in the cart by its ID
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),

    # URL for placing the order after cart review
    path('place_order/', views.place_order, name='place_order'),

    # Order summary page URL for reviewing details of a specific order
    path('order/<int:order_id>/summary/', views.order_summary, name='order_summary'),

    # Checkout page URL for proceeding to payment
    path('checkout/', views.checkout, name='checkout'),

    # Page to show payment success after transaction completion
    path('payment-successful/', views.payment_successful, name='payment-successful'),

    # Page to show payment failure message after a failed transaction
    path('payment-failed/', views.payment_failed, name='payment-failed'),

    # URL for displaying all orders placed by farmers
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),

    # URL for updating the status of an order item by its ID
    path('order-item/<int:item_id>/update-status/', views.update_order_item_status, name='update_order_item_status'),
]
