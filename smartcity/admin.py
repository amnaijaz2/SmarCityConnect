from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ServiceProviderR, CustomerR, ActivityLog, Notification

# Service Provider Inline for User adminfrom django.contrib import admin
from .models import ServiceProviderR, CustomerR, ActivityLog, Notification

@admin.register(ServiceProviderR)
class ServiceProviderRAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'servicename', 'Phoneno', 'is_approved', 'rating')
    list_filter = ('servicename', 'is_approved')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'address')
    list_editable = ('is_approved',)
    readonly_fields = ('password',)
    actions = ['approve_providers', 'disapprove_providers']
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'Phoneno', 'address')
        }),
        ('Service Information', {
            'fields': ('service_image', 'servicename', 'description')
        }),
        ('Status', {
            'fields': ('is_approved', 'rating')
        }),
    )
    
    def approve_providers(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected providers have been approved.")
    approve_providers.short_description = "Approve selected providers"
    
    def disapprove_providers(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected providers have been disapproved.")
    disapprove_providers.short_description = "Disapprove selected providers"

@admin.register(CustomerR)
class CustomerRAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('password',)
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name')
        }),
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'message', 'timestamp', 'related_provider', 'related_customer')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('message', 'related_provider__username', 'related_customer__username')
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('activity_type', 'message', 'timestamp')
        }),
        ('Related Entities', {
            'fields': ('related_provider', 'related_customer'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'is_read', 'created_at', 'get_recipient')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Recipient', {
            'fields': ('user',)
        }),
        ('Notification Content', {
            'fields': ('notification_type', 'title', 'message', 'link')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def get_recipient(self, obj):
        return obj.user.username
    get_recipient.short_description = 'Recipient'