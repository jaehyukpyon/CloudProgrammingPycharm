from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('buy/', views.buy),
    path('sell/', views.sell),
]