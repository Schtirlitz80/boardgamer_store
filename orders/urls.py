from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'order'

urlpatterns = [
    path('basket_adding', views.basket_adding, name='basket_adding'),
]