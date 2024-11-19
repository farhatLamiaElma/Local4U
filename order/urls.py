from django.urls import path

from MyChatBot.urls import urlpatterns
from . import views

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
]