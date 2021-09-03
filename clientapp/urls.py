from django.http import request
from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    
    path('', views.clhome, name='cllogin'),
    path('clhome/', views.clhome, name='clhome'),
    path('clabout/', views.clabout, name='clabout'),
    path('clregister/', views.clregister, name='clregister'),
    path('clotp/', views.clotp, name='clotp'),
]