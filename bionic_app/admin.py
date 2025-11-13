"""
Django Admin Configuration for Bionic Hand System
"""
from django.contrib import admin
from .models import Component, SimulationLog, ResearchFile, ContactMessage, Progress

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(SimulationLog)
class SimulationLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'timestamp']
    search_fields = ['action', 'user']
    list_filter = ['timestamp', 'action']
    readonly_fields = ['timestamp']

@admin.register(ResearchFile)
class ResearchFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_on']
    search_fields = ['title']
    list_filter = ['uploaded_on']
    readonly_fields = ['uploaded_on']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'description']
    list_filter = ['date']
    date_hierarchy = 'date'
