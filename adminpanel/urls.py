from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.loginView, name='admin-login'),
    path("logout", views.logoutUser, name='admin-logout'),
    path("dashboard", views.dashboard, name='dashboard'),
    path("gallery", views.showGallery, name='gallery'),
    path("item-details/<int:id>", views.itemDetails, name='auction-item-details'),
]
