from django.urls import path
from . import views

app_name = 'app_login'

urlpatterns = [
    path(r'index/', views.index),
    path(r'login/', views.login),
    path(r'register/', views.register),
    path(r'logout/', views.logout),
]

