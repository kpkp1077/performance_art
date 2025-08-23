from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from decimal import Decimal
from .models import CompensationPlan, Commission, CommissionPayout, UserCompensationPlan
from .serializers import (
    CompensationPlanSerializer, CommissionSerializer, CommissionPayoutSerializer,
    UserCompensationPlanSerializer, CommissionSummarySerializer
)
from .utils import CommissionCalculator


class CompensationPlanListCreateView(generics.ListCreateAPIView):
    """List and create compensation plans"""
    queryset = CompensationPlan.objects.filter(is_active=True)
    serializer_class = CompensationPlanSerializer
    permission_classes = [IsAuthenticated]


class CompensationPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Compensation plan detail view"""
    queryset = CompensationPlan.objects.all()
    serializer_class = CompensationPlanSerializer
    permission_classes = [IsAuthenticated]


class UserCompensationPlanListCreateView(generics.ListCreateAPIView):
    """List and create user compensation plan assignments"""
    serializer_class = UserCompensationPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserCompensationPlan.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(user=user)
        
        return queryset.select_related('user', 'compensation_plan')


class CommissionListView(generics.ListAPIView):
    """List commissions"""
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Commission.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(user=user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('user', 'deal', 'compensation_plan')


class CommissionDetailView(generics.RetrieveUpdateAPIView):
    """Commission detail view"""
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]


class CommissionPayoutListCreateView(generics.ListCreateAPIView):
    """List and create commission payouts"""
    serializer_class = CommissionPayoutSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = CommissionPayout.objects.all()
        user = self.request.user
        
        # Filter by current user if they're a rep
        if user.role == 'rep':
            queryset = queryset.filter(user=user)
        
        return queryset.select_related('user')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_commissions(request):
    """Bulk calculate commissions for closed deals"""
    calculator = CommissionCalculator()
    
    # Get deals to process
    deal_ids = request.data.get('deal_ids', [])
    if deal_ids:
        from sales.models import Deal
        deals = Deal.objects.filter(id__in=deal_ids, status='closed_won')
    else:
        # Process all unprocessed closed deals
        deals = None
    
    try:
        commissions_created = calculator.bulk_calculate_commissions(deals)
        return Response({
            'message': f'Successfully calculated {len(commissions_created)} commissions',
            'commission_ids': [c.id for c in commissions_created]
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_summary(request):
    """Get commission summary statistics"""
    user = request.user
    
    # Base queryset
    if user.role == 'rep':
        commissions_qs = Commission.objects.filter(user=user)
    else:
        commissions_qs = Commission.objects.all()
    
    # Calculate statistics
    total_commissions = commissions_qs.aggregate(Sum('commission_amount'))['commission_amount__sum'] or Decimal('0')
    pending_commissions = commissions_qs.filter(status='pending').aggregate(Sum('commission_amount'))['commission_amount__sum'] or Decimal('0')
    paid_commissions = commissions_qs.filter(status='paid').aggregate(Sum('commission_amount'))['commission_amount__sum'] or Decimal('0')
    commission_count = commissions_qs.count()
    average_commission = commissions_qs.aggregate(Avg('commission_amount'))['commission_amount__avg'] or Decimal('0')
    
    data = {
        'total_commissions': total_commissions,
        'pending_commissions': pending_commissions,
        'paid_commissions': paid_commissions,
        'commission_count': commission_count,
        'average_commission': average_commission
    }
    
    serializer = CommissionSummarySerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_analytics(request):
    """Get commission analytics using Pandas"""
    calculator = CommissionCalculator()
    user = request.user
    
    # Get query parameters
    user_id = request.query_params.get('user_id') if user.role != 'rep' else user.id
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    try:
        # Generate commission report
        df = calculator.generate_commission_report(user_id, start_date, end_date)
        
        if df.empty:
            return Response({'message': 'No commission data found'})
        
        # Calculate analytics
        monthly_stats = df.groupby('month').agg({
            'commission_amount': ['sum', 'count', 'mean'],
            'deal_amount': 'sum'
        }).round(2)
        
        # Top performers
        top_performers = calculator.get_top_performers(limit=5)
        
        analytics_data = {
            'total_records': len(df),
            'date_range': {
                'start': str(df['calculation_date'].min()),
                'end': str(df['calculation_date'].max())
            },
            'monthly_stats': monthly_stats.to_dict() if not monthly_stats.empty else {},
            'top_performers': top_performers.to_dict('records') if not top_performers.empty else [],
            'average_commission_rate': float(df['commission_rate'].mean()),
            'total_commission_amount': float(df['commission_amount'].sum())
        }
        
        return Response(analytics_data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_projections(request):
    """Get commission payout projections"""
    calculator = CommissionCalculator()
    user = request.user
    
    user_id = request.query_params.get('user_id') if user.role != 'rep' else user.id
    months = int(request.query_params.get('months', 3))
    
    try:
        projections = calculator.calculate_payout_projections(user_id, months)
        return Response(projections)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commission_trends(request):
    """Get commission trends analysis"""
    calculator = CommissionCalculator()
    user = request.user
    
    user_id = request.query_params.get('user_id') if user.role != 'rep' else user.id
    
    try:
        # Get last 12 months of data
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        end_date = datetime.now().date()
        start_date = end_date - relativedelta(months=12)
        
        df = calculator.generate_commission_report(user_id, start_date, end_date)
        
        if df.empty:
            return Response({'message': 'No data available for trends analysis'})
        
        # Monthly trends
        monthly_trends = df.groupby('month').agg({
            'commission_amount': 'sum',
            'deal_amount': 'sum'
        }).reset_index()
        
        monthly_trends['month'] = monthly_trends['month'].astype(str)
        
        # Calculate growth rates
        monthly_trends['commission_growth'] = monthly_trends['commission_amount'].pct_change() * 100
        monthly_trends['deal_growth'] = monthly_trends['deal_amount'].pct_change() * 100
        
        # Plan type distribution
        plan_distribution = df.groupby('plan_name').agg({
            'commission_amount': 'sum'
        }).reset_index()
        
        trends_data = {
            'monthly_trends': monthly_trends.fillna(0).to_dict('records'),
            'plan_distribution': plan_distribution.to_dict('records'),
            'average_monthly_commission': float(monthly_trends['commission_amount'].mean()),
            'highest_month': monthly_trends.loc[monthly_trends['commission_amount'].idxmax()].to_dict() if not monthly_trends.empty else {},
            'growth_trend': 'positive' if monthly_trends['commission_growth'].tail(3).mean() > 0 else 'negative'
        }
        
        return Response(trends_data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)