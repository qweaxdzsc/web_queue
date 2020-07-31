from django.contrib import admin
# superuser account bzmbn4 pwd abc=123456
# Register your models here.
from . import models

admin.site.register(models.User)