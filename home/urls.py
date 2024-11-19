from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('FAQ/<int:farmer_id>/', views.FAQ, name='FAQ'),

]