from django.contrib import admin
from .models import CompensationPlan, CommissionRule, UserCompensationPlan, Commission, CommissionPayout


class CommissionRuleInline(admin.TabularInline):
    model = CommissionRule
    extra = 1


@admin.register(CompensationPlan)
class CompensationPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'base_rate', 'is_active', 'created_at')
    list_filter = ('plan_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    inlines = [CommissionRuleInline]


@admin.register(UserCompensationPlan)
class UserCompensationPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'compensation_plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('compensation_plan', 'is_active', 'start_date')
    search_fields = ('user__username', 'compensation_plan__name')
    date_hierarchy = 'start_date'


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'deal', 'commission_amount', 'status', 'calculation_date')
    list_filter = ('status', 'calculation_date', 'compensation_plan')
    search_fields = ('user__username', 'deal__name')
    date_hierarchy = 'calculation_date'
    readonly_fields = ('calculation_date',)


@admin.register(CommissionPayout)
class CommissionPayoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'period_start', 'period_end', 'total_amount', 'status')
    list_filter = ('status', 'period_start')
    search_fields = ('user__username',)
    date_hierarchy = 'period_start'