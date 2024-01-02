from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index , name = 'Extractive'),
    path('Extractive/', views.index , name = "Extractive"),
    path('Abstractive/', views.index2 , name = 'Abstractive'),

]