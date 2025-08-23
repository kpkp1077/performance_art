import pandas as pd
import numpy as np
from decimal import Decimal
from django.db.models import Q
from sales.models import Deal
from .models import CompensationPlan, Commission, UserCompensationPlan


class CommissionCalculator:
    """Commission calculation utility using Pandas"""
    
    def __init__(self):
        self.commission_data = []
    
    def calculate_deal_commission(self, deal, user_compensation_plan):
        """Calculate commission for a single deal"""
        plan = user_compensation_plan.compensation_plan
        deal_amount = deal.amount
        
        if plan.plan_type == 'flat_rate':
            return plan.base_rate
        elif plan.plan_type == 'percentage':
            return deal_amount * (plan.base_rate / 100)
        elif plan.plan_type == 'tiered':
            return self._calculate_tiered_commission(deal_amount, plan)
        elif plan.plan_type == 'quota_based':
            return self._calculate_quota_based_commission(deal, user_compensation_plan)
        
        return Decimal('0')
    
    def _calculate_tiered_commission(self, deal_amount, plan):
        """Calculate tiered commission using rules"""
        commission = Decimal('0')
        remaining_amount = deal_amount
        
        for rule in plan.rules.all().order_by('order'):
            if remaining_amount <= 0:
                break
            
            tier_min = rule.min_amount or Decimal('0')
            tier_max = rule.max_amount or remaining_amount
            
            if remaining_amount > tier_min:
                tier_amount = min(remaining_amount - tier_min, tier_max - tier_min)
                commission += tier_amount * (rule.commission_rate / 100)
                remaining_amount -= tier_amount
        
        return commission
    
    def _calculate_quota_based_commission(self, deal, user_compensation_plan):
        """Calculate quota-based commission with accelerators"""
        from sales.models import Quota
        
        plan = user_compensation_plan.compensation_plan
        user = deal.owner
        
        # Get current quota for the deal period
        quota = Quota.objects.filter(
            user=user,
            start_date__lte=deal.close_date,
            end_date__gte=deal.close_date
        ).first()
        
        if not quota:
            # No quota, use base rate
            return deal.amount * (plan.base_rate / 100)
        
        # Calculate quota attainment
        closed_deals = Deal.objects.filter(
            owner=user,
            status='closed_won',
            close_date__gte=quota.start_date,
            close_date__lte=quota.end_date
        ).exclude(id=deal.id)
        
        current_attainment = sum(d.amount for d in closed_deals)
        new_attainment = current_attainment + deal.amount
        
        # Apply accelerator if over threshold
        if (plan.threshold_amount and 
            new_attainment >= plan.threshold_amount and 
            plan.accelerator_rate):
            return deal.amount * (plan.accelerator_rate / 100)
        else:
            return deal.amount * (plan.base_rate / 100)
    
    def bulk_calculate_commissions(self, deals_queryset=None):
        """Bulk calculate commissions using Pandas for performance"""
        if deals_queryset is None:
            deals_queryset = Deal.objects.filter(status='closed_won', commissions__isnull=True)
        
        # Convert to DataFrame for efficient processing
        deals_data = []
        for deal in deals_queryset.select_related('owner'):
            user_plan = UserCompensationPlan.objects.filter(
                user=deal.owner,
                is_active=True,
                start_date__lte=deal.close_date,
                Q(end_date__isnull=True) | Q(end_date__gte=deal.close_date)
            ).first()
            
            if user_plan:
                deals_data.append({
                    'deal_id': deal.id,
                    'user_id': deal.owner.id,
                    'amount': float(deal.amount),
                    'close_date': deal.close_date,
                    'plan_type': user_plan.compensation_plan.plan_type,
                    'base_rate': float(user_plan.compensation_plan.base_rate),
                    'plan_id': user_plan.compensation_plan.id
                })
        
                        if not deals_data:
            return []

        df = pd.DataFrame(deals_data)
        
        # Vectorized commission calculations for simple types
        mask_percentage = df['plan_type'] == 'percentage'
        df.loc[mask_percentage, 'commission'] = (
            df.loc[mask_percentage, 'amount'] * 
            df.loc[mask_percentage, 'base_rate'] / 100
        )
        
        mask_flat = df['plan_type'] == 'flat_rate'
        df.loc[mask_flat, 'commission'] = df.loc[mask_flat, 'base_rate']
        
        # Handle complex calculations individually
        complex_types = ['tiered', 'quota_based']
        for _, row in df[df['plan_type'].isin(complex_types)].iterrows():
            deal = Deal.objects.get(id=row['deal_id'])
            user_plan = UserCompensationPlan.objects.get(
                user_id=row['user_id'],
                compensation_plan_id=row['plan_id'],
                is_active=True
            )
            commission = self.calculate_deal_commission(deal, user_plan)
            df.loc[df['deal_id'] == row['deal_id'], 'commission'] = float(commission)
        
        # Create commission records
        commissions_created = []
        for _, row in df.iterrows():
            deal = Deal.objects.get(id=row['deal_id'])
            plan = CompensationPlan.objects.get(id=row['plan_id'])
            
            commission = Commission.objects.create(
                user_id=row['user_id'],
                deal=deal,
                compensation_plan=plan,
                commission_amount=Decimal(str(row['commission'])),
                commission_rate=Decimal(str(row['base_rate'])),
                deal_amount=deal.amount,
                status='calculated'
            )
            commissions_created.append(commission)
        
        return commissions_created
    
    def generate_commission_report(self, user_id=None, start_date=None, end_date=None):
        """Generate commission analytics report using Pandas"""
        queryset = Commission.objects.all()
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(calculation_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(calculation_date__lte=end_date)
        
        # Convert to DataFrame
        data = []
        for commission in queryset.select_related('user', 'deal', 'compensation_plan'):
            data.append({
                'user_name': commission.user.get_full_name(),
                'deal_name': commission.deal.name,
                'plan_name': commission.compensation_plan.name,
                'deal_amount': float(commission.deal_amount),
                'commission_amount': float(commission.commission_amount),
                'commission_rate': float(commission.commission_rate),
                'status': commission.status,
                'calculation_date': commission.calculation_date.date(),
                'payment_date': commission.payment_date
            })
        
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Add analytics columns
        df['commission_percentage'] = (df['commission_amount'] / df['deal_amount']) * 100
        df['month'] = pd.to_datetime(df['calculation_date']).dt.to_period('M')
        
        return df
    
    def get_top_performers(self, period='monthly', limit=10):
        """Get top performing sales reps by commission"""
        df = self.generate_commission_report()
        
        if df.empty:
            return pd.DataFrame()
        
        if period == 'monthly':
            grouped = df.groupby(['user_name', 'month']).agg({
                'commission_amount': 'sum',
                'deal_amount': 'sum'
            }).reset_index()
        else:
            grouped = df.groupby('user_name').agg({
                'commission_amount': 'sum',
                'deal_amount': 'sum'
            }).reset_index()
        
        return grouped.nlargest(limit, 'commission_amount')
    
    def calculate_payout_projections(self, user_id, projection_months=3):
        """Calculate commission payout projections"""
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta
        
        # Get historical data
        end_date = datetime.now().date()
        start_date = end_date - relativedelta(months=6)
        
        df = self.generate_commission_report(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if df.empty:
            return {}
        
        # Calculate monthly averages
        monthly_avg = df.groupby('month')['commission_amount'].sum().mean()
        
        # Project future months
        projections = []
        current_date = end_date
        
        for i in range(projection_months):
            current_date = current_date + relativedelta(months=1)
            projections.append({
                'month': current_date.strftime('%Y-%m'),
                'projected_commission': float(monthly_avg),
                'confidence': 0.8 - (i * 0.1)  # Decreasing confidence over time
            })
        
        return {
            'historical_average': float(monthly_avg),
            'projections': projections,
            'data_points': len(df)
        }