from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name='index'),
    path("logout", views.logout, name='logout'),
    path("create-item", views.create, name='create-item'),
    path("my-posted-items", views.showMyItems, name='my-posted-items'),
    path("item-details/<int:id>", views.itemDetails, name='item-details'),
    
]
