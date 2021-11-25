from django.contrib import admin

from .models import *


@admin.register(Users)
class Users(admin.ModelAdmin):
    fields = ["last_name", "first_name", "middle_name", "position",
              "department", "password", "created", "is_active"]
    list_display = ["pk", "last_name", "created"]
    readonly_fields = ["is_active"]
    search_fields = ["last_name"]


@admin.register(NotifyError)
class NotifyErrorAdmin(admin.ModelAdmin):
    fields = ["last_name", "text", "created"]
    list_display = ["pk", "last_name", "created"]
    search_fields = ["last_name"]
