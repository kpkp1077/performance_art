from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, Q
from decimal import Decimal
from .models import Deal, Quota, SalesActivity
from .serializers import (
    DealSerializer, QuotaSerializer, SalesActivitySerializer, DealSummarySerializer
)


class DealListCreateView(generics.ListCreateAPIView):
    """List and create deals"""
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Deal.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(owner=user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by stage
        stage_filter = self.request.query_params.get('stage')
        if stage_filter:
            queryset = queryset.filter(stage=stage_filter)
        
        return queryset.select_related('owner')
    
    def perform_create(self, serializer):
        # Set the owner to current user if not specified
        if not serializer.validated_data.get('owner'):
            serializer.save(owner=self.request.user)
        else:
            serializer.save()


class DealDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Deal detail view"""
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]


class QuotaListCreateView(generics.ListCreateAPIView):
    """List and create quotas"""
    serializer_class = QuotaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Quota.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(user=user)
        
        return queryset.select_related('user')


class QuotaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Quota detail view"""
    queryset = Quota.objects.all()
    serializer_class = QuotaSerializer
    permission_classes = [IsAuthenticated]


class SalesActivityListCreateView(generics.ListCreateAPIView):
    """List and create sales activities"""
    serializer_class = SalesActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = SalesActivity.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(user=user)
        
        # Filter by deal
        deal_id = self.request.query_params.get('deal')
        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)
        
        return queryset.select_related('user', 'deal')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    user = request.user
    
    # Base queryset
    if user.role == 'rep':
        deals_qs = Deal.objects.filter(owner=user)
    else:
        deals_qs = Deal.objects.all()
    
    # Calculate statistics
    total_deals = deals_qs.count()
    total_value = deals_qs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    won_deals = deals_qs.filter(status='closed_won').count()
    won_value = deals_qs.filter(status='closed_won').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    lost_deals = deals_qs.filter(status='closed_lost').count()
    open_deals = deals_qs.filter(status='open').count()
    
    avg_deal_size = deals_qs.aggregate(Avg('amount'))['amount__avg'] or Decimal('0')
    
    # Calculate win rate
    closed_deals = won_deals + lost_deals
    win_rate = Decimal('0')
    if closed_deals > 0:
        win_rate = (Decimal(won_deals) / Decimal(closed_deals)) * Decimal('100')
    
    data = {
        'total_deals': total_deals,
        'total_value': total_value,
        'won_deals': won_deals,
        'won_value': won_value,
        'lost_deals': lost_deals,
        'open_deals': open_deals,
        'average_deal_size': avg_deal_size,
        'win_rate': win_rate.quantize(Decimal('0.01'))
    }
    
    serializer = DealSummarySerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pipeline_analysis(request):
    """Get pipeline analysis by stage"""
    user = request.user
    
    # Base queryset
    if user.role == 'rep':
        deals_qs = Deal.objects.filter(owner=user, status='open')
    else:
        deals_qs = Deal.objects.filter(status='open')
    
    # Group by stage
    pipeline_data = deals_qs.values('stage').annotate(
        count=Count('id'),
        total_value=Sum('amount'),
        avg_probability=Avg('probability')
    ).order_by('stage')
    
    return Response(list(pipeline_data))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quota_performance(request):
    """Get quota performance data"""
    user = request.user
    
    # Base queryset
    if user.role == 'rep':
        quotas_qs = Quota.objects.filter(user=user)
    else:
        quotas_qs = Quota.objects.all()
    
    quota_data = []
    for quota in quotas_qs.select_related('user'):
        # Calculate attainment
        closed_deals = Deal.objects.filter(
            owner=quota.user,
            status='closed_won',
            close_date__gte=quota.start_date,
            close_date__lte=quota.end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        attainment_pct = Decimal('0')
        if quota.amount > 0:
            attainment_pct = (closed_deals / quota.amount) * Decimal('100')
        
        quota_data.append({
            'id': quota.id,
            'user_name': quota.user.get_full_name(),
            'period': quota.period,
            'quota_amount': quota.amount,
            'achieved_amount': closed_deals,
            'attainment_percentage': attainment_pct.quantize(Decimal('0.01')),
            'start_date': quota.start_date,
            'end_date': quota.end_date
        })
    
    return Response(quota_data)