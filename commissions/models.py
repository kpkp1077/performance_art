from django.db import models
from django.contrib.auth import get_user_model
from sales.models import Deal

User = get_user_model()


class CompensationPlan(models.Model):
    """Compensation plan model"""
    
    PLAN_TYPES = [
        ('flat_rate', 'Flat Rate'),
        ('percentage', 'Percentage'),
        ('tiered', 'Tiered'),
        ('quota_based', 'Quota Based'),
    ]
    
    name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    base_rate = models.DecimalField(max_digits=10, decimal_places=4, help_text="Base commission rate")
    threshold_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    accelerator_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class CommissionRule(models.Model):
    """Commission rule for specific conditions"""
    
    compensation_plan = models.ForeignKey(CompensationPlan, on_delete=models.CASCADE, related_name='rules')
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=4)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.compensation_plan.name} - Rule {self.order}"
    
    class Meta:
        ordering = ['compensation_plan', 'order']


class UserCompensationPlan(models.Model):
    """Association between users and compensation plans"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compensation_plans')
    compensation_plan = models.ForeignKey(CompensationPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.compensation_plan.name}"
    
    class Meta:
        unique_together = ['user', 'compensation_plan', 'start_date']


class Commission(models.Model):
    """Individual commission calculation"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('calculated', 'Calculated'),
        ('paid', 'Paid'),
        ('disputed', 'Disputed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='commissions')
    compensation_plan = models.ForeignKey(CompensationPlan, on_delete=models.CASCADE)
    commission_amount = models.DecimalField(max_digits=15, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=4)
    deal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    calculation_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.deal.name} - ${self.commission_amount}"
    
    class Meta:
        ordering = ['-calculation_date']


class CommissionPayout(models.Model):
    """Commission payout batches"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payouts')
    period_start = models.DateField()
    period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    commissions = models.ManyToManyField(Commission, related_name='payouts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    processed_date = models.DateTimeField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.period_start} to {self.period_end} - ${self.total_amount}"
    
    class Meta:
        ordering = ['-period_end']