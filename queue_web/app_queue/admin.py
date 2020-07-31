from django.contrib import admin
# Register your models here.
from . import models


class WaitListAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'account_email', 'sender_address', 'mission_name', 'mission_data',
                    'register_time', ]
    search_fields = ['id', 'order_id', 'account_email', 'sender_address', 'mission_name']
    list_filter = ['id', 'order_id', 'sender_address', 'register_time', ]
    ordering = ['order_id']


class RunningListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'mission_data',
                    'register_time', 'start_time']
    search_fields = ['id', 'account_email', 'sender_address', 'mission_name']
    list_filter = ['id', 'sender_address', 'register_time', 'start_time']
    ordering = ['start_time']


class HistoryListAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_email', 'sender_address', 'mission_name', 'mission_data',
                    'register_time', 'start_time', 'used_time']
    search_fields = ['id',  'account_email', 'sender_address', 'mission_name']
    list_filter = ['id', 'sender_address', 'register_time', 'start_time', 'used_time']
    ordering = ['id']


admin.site.register(models.WaitList, WaitListAdmin)
admin.site.register(models.RunningList, RunningListAdmin)
admin.site.register(models.HistoryList, HistoryListAdmin)