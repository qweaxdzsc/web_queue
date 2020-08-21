from django.contrib import admin
# Register your models here.
from . import models


class WaitListAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'account_email', 'sender_address', 'exec_app', 'mission_name', 'mission_data',
                    'register_time', ]
    search_fields = ['id', 'order_id', 'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'order_id', 'sender_address', 'register_time', 'exec_app', ]
    ordering = ['order_id']


class RunningListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'mission_data', 'exec_app',
                    'register_time', 'start_time']
    search_fields = ['id', 'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'sender_address', 'register_time', 'start_time', 'exec_app', ]
    ordering = ['start_time']


class HistoryListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'mission_data', 'exec_app',
                    'register_time', 'start_time', 'used_time']
    search_fields = ['id',  'account_email', 'sender_address', 'mission_name', 'exec_app', ]
    list_filter = ['id', 'sender_address', 'register_time', 'start_time', 'used_time', 'exec_app', ]
    ordering = ['id']


admin.site.register(models.WaitList, WaitListAdmin)
admin.site.register(models.RunningList, RunningListAdmin)
admin.site.register(models.HistoryList, HistoryListAdmin)