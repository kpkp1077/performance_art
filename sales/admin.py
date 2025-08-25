from django.contrib import admin
from .models import Deal, Quota, SalesActivity


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_name', 'owner', 'amount', 'status', 'stage', 'close_date')
    list_filter = ('status', 'stage', 'created_date', 'close_date')
    search_fields = ('name', 'account_name', 'owner__username')
    date_hierarchy = 'close_date'
    ordering = ('-created_date',)


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'period', 'start_date', 'end_date')
    list_filter = ('period', 'start_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    date_hierarchy = 'start_date'


@admin.register(SalesActivity)
class SalesActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'subject', 'deal', 'user', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('subject', 'deal__name', 'user__username')
    date_hierarchy = 'created_at'