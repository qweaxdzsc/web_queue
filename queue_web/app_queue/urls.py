from django.urls import path
from . import views
from . import thread_queue

app_name = 'app_queue'

urlpatterns = [
    path(r'', views.index),
    path(r'add/', views.AddProject.as_view()),
    path(r'search_list/', views.fetch_tables),
    path(r'get_local_file/', views.get_local_file),
    path(r'receive_result/', views.receive_result),
    path(r'get_csrf/', views.get_csrf),
]