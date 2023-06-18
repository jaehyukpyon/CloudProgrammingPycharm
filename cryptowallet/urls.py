from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_),
    path('history', views.history),
    path('setting', views.setting),
    path('logout', views.logout_),
    path('register', views.register_),
]