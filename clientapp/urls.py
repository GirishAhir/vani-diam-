from django.http import request
from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    
    path('', views.clhome, name='clhome'),
    path('clhome/', views.clhome, name='clhome'),
    path('clabout/', views.clabout, name='clabout'),
    path('clregister/', views.clregister, name='clregister'),
    path('clotp/', views.clotp, name='clotp'),
    path('cllogin/', views.cllogin, name='cllogin'),
    path('clcontact/', views.clcontact,name='clcontact'),
    path('cllogout/', views.cllogout, name='cllogout'),
    path('clcollection/', views.clcollection, name='clcollection'),
    path('clforgot1/', views.clforgot1, name='clforgot1'),
    path('clforgot2/', views.clforgot2, name='clforgot2'), 
    path('clforgot3/', views.clforgot3, name='clforgot3')

]