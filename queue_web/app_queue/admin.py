from django.contrib import admin
# Register your models here.
from . import models

"""
password: abc=123456
controls the display style in '/admin' website
"""


class WaitListAdmin(admin.ModelAdmin):
    """
    The variable name are fixed

    list_display: the table head
    search_fields: determine which field will be include in search criteria
    list_filter: determine which field can be used as filter
    ordering: determine the sequence of showing items
    """
    list_display = ['id', 'order_id', 'account_email', 'sender_address', 'exec_app', 'mission_name',
                    'short_mission_data', 'register_time', ]
    search_fields = ['id', 'order_id', 'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'order_id', 'sender_address', 'register_time', 'exec_app', ]
    ordering = ['order_id']


class RunningListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'short_mission_data', 'exec_app',
                    'register_time', 'start_time']
    search_fields = ['id', 'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'sender_address', 'register_time', 'start_time', 'exec_app', ]
    ordering = ['start_time']


class HistoryListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'short_mission_data', 'exec_app',
                    'register_time', 'start_time', 'used_time']
    search_fields = ['id',  'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'sender_address', 'register_time', 'start_time', 'used_time', 'exec_app', ]
    ordering = ['id']


# register the class into admin site
admin.site.register(models.WaitList, WaitListAdmin)
admin.site.register(models.RunningList, RunningListAdmin)
admin.site.register(models.HistoryList, HistoryListAdmin)