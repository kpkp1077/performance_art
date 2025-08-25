from rest_framework import serializers
from .models import CompensationPlan, CommissionRule, UserCompensationPlan, Commission, CommissionPayout


class CommissionRuleSerializer(serializers.ModelSerializer):
    """Commission rule serializer"""
    
    class Meta:
        model = CommissionRule
        fields = ['id', 'min_amount', 'max_amount', 'commission_rate', 'order']


class CompensationPlanSerializer(serializers.ModelSerializer):
    """Compensation plan serializer"""
    rules = CommissionRuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = CompensationPlan
        fields = ['id', 'name', 'plan_type', 'base_rate', 'threshold_amount',
                 'accelerator_rate', 'is_active', 'description', 'created_at',
                 'updated_at', 'rules']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCompensationPlanSerializer(serializers.ModelSerializer):
    """User compensation plan serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    plan_name = serializers.CharField(source='compensation_plan.name', read_only=True)
    
    class Meta:
        model = UserCompensationPlan
        fields = ['id', 'user', 'user_name', 'compensation_plan', 'plan_name',
                 'start_date', 'end_date', 'is_active']
        read_only_fields = ['id']


class CommissionSerializer(serializers.ModelSerializer):
    """Commission serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    deal_name = serializers.CharField(source='deal.name', read_only=True)
    plan_name = serializers.CharField(source='compensation_plan.name', read_only=True)
    
    class Meta:
        model = Commission
        fields = ['id', 'user', 'user_name', 'deal', 'deal_name', 'compensation_plan',
                 'plan_name', 'commission_amount', 'commission_rate', 'deal_amount',
                 'status', 'calculation_date', 'payment_date', 'notes']
        read_only_fields = ['id', 'calculation_date']


class CommissionPayoutSerializer(serializers.ModelSerializer):
    """Commission payout serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    commission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CommissionPayout
        fields = ['id', 'user', 'user_name', 'period_start', 'period_end',
                 'total_amount', 'status', 'processed_date', 'payment_date',
                 'commission_count']
        read_only_fields = ['id']
    
    def get_commission_count(self, obj):
        return obj.commissions.count()


class CommissionSummarySerializer(serializers.Serializer):
    """Commission summary statistics"""
    total_commissions = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_commissions = serializers.DecimalField(max_digits=15, decimal_places=2)
    paid_commissions = serializers.DecimalField(max_digits=15, decimal_places=2)
    commission_count = serializers.IntegerField()
    average_commission = serializers.DecimalField(max_digits=15, decimal_places=2)