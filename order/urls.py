from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('place_order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/summary/', views.order_summary, name='order_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-successful/', views.payment_successful, name='payment-successful'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
    path('order-item/<int:item_id>/update-status/', views.update_order_item_status, name='update_order_item_status'),
]