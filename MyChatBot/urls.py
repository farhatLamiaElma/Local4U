from django.urls import path

#from Products.urls import urlpatterns
from . import views
from .views import chat


urlpatterns = [
    path('chat/', views.chat, name='chat'),
]