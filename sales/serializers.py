from rest_framework import serializers
from .models import Deal, Quota, SalesActivity


class DealSerializer(serializers.ModelSerializer):
    """Deal serializer"""
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    days_since_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Deal
        fields = ['id', 'name', 'account_name', 'owner', 'owner_name', 'amount',
                 'status', 'stage', 'probability', 'close_date', 'created_date',
                 'last_activity', 'description', 'days_since_created']
        read_only_fields = ['id', 'created_date', 'last_activity']
    
    def get_days_since_created(self, obj):
        from django.utils import timezone
        return (timezone.now().date() - obj.created_date).days


class QuotaSerializer(serializers.ModelSerializer):
    """Quota serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    attainment_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Quota
        fields = ['id', 'user', 'user_name', 'amount', 'period', 'start_date',
                 'end_date', 'created_at', 'attainment_percentage']
        read_only_fields = ['id', 'created_at']
    
    def get_attainment_percentage(self, obj):
        # Calculate attainment based on closed won deals in the period
        from django.db.models import Sum
        closed_deals = Deal.objects.filter(
            owner=obj.user,
            status='closed_won',
            close_date__gte=obj.start_date,
            close_date__lte=obj.end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if obj.amount > 0:
            return round((closed_deals / obj.amount) * 100, 2)
        return 0


class SalesActivitySerializer(serializers.ModelSerializer):
    """Sales activity serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    deal_name = serializers.CharField(source='deal.name', read_only=True)
    
    class Meta:
        model = SalesActivity
        fields = ['id', 'deal', 'deal_name', 'user', 'user_name', 'activity_type',
                 'subject', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class DealSummarySerializer(serializers.Serializer):
    """Deal summary statistics"""
    total_deals = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    won_deals = serializers.IntegerField()
    won_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    lost_deals = serializers.IntegerField()
    open_deals = serializers.IntegerField()
    average_deal_size = serializers.DecimalField(max_digits=15, decimal_places=2)
    win_rate = serializers.DecimalField(max_digits=5, decimal_places=2)