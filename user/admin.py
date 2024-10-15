from django.contrib import admin
from user.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username',]
