from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Model Task"""
    list_display = ["title", "user", "date_create", "execute_status"]
    list_display_links = ["title"]
    list_filter = ["execute_status"]
    list_editable = ["execute_status"]
