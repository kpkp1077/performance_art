from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SalesTeam


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'employee_id', 'phone', 'hire_date', 'is_active_sales')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active_sales')
    list_filter = BaseUserAdmin.list_filter + ('role', 'is_active_sales')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')


@admin.register(SalesTeam)
class SalesTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'manager__username')