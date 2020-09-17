from django.urls import path, include
from . import api_views

app_name = 'app_queue'


# dispatched from  url '/api/'
urlpatterns = [
    path(r'', api_views.help),
    path(r'add/', api_views.api_add),
    path(r'search_list/', api_views.api_history),
    path(r'pause/', api_views.api_suspend),
]