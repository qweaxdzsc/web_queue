from django.urls import path, include
from . import views
# from . import thread_queue

app_name = 'app_queue'

# url route
urlpatterns = [
    path('api/', include('app_queue.api.api_urls', namespace='api_urls')),  # api branch connect
    path(r'', views.index),
    path(r'add/', views.AddProject.as_view()),
    path(r'search_list/', views.fetch_tables),
    path(r'get_local_file/', views.get_local_file),
    path(r'receive_result/', views.receive_result),
    path(r'get_csrf/', views.get_csrf),
    path(r'pause/', views.pause_queue),
    path(r'reorder/', views.queue_reorder),
    path(r'test/', views.test),
    path(r'test_post/', views.test_post),
]