from django.urls import path
from .views import clients_main

urlpatterns = [
    path('',clients_main,name='clients_main'),
]