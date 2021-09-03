from django.http import request
from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('collection/', views.collection, name='collection'),
    path('single/', views.single, name='single'),
    path('login/', views.login, name='login'),
    path('otp/', views.otp, name='otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fpassword1/', views.fpassword1, name='fpassword1'),
    path('fpassword2/', views.fpassword2, name='fpassword2'),
    path('fpassword3/', views.fpassword3, name='fpassword3'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('add-event/', views.add_event, name='add-event'),
    path('all-event/', views.all_event, name='all-event'),
    path('edit-event/<int:pk>', views.edit_event, name='edit-event'),
    path('delete-event/<int:pk>', views.delete_event, name='delete-event'),

  

]
