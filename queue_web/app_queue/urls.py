from django.urls import path
from . import views

app_name = 'app_queue'

urlpatterns = [
    path(r'', views.index),
    path(r'add/', views.add_project),
    path(r'search_list/', views.fetch_tables),
    path(r'get_local_file/', views.get_local_file),
    path(r'receive_result/', views.receive_result),
]

