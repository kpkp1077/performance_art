from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Deal(models.Model):
    """Sales deal/opportunity model"""
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    account_name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    probability = models.IntegerField(default=50, help_text="Probability of closing (%)")
    close_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.account_name} (${self.amount})"
    
    class Meta:
        ordering = ['-created_date']


class Quota(models.Model):
    """Sales quota model"""
    
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotas')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.period} ${self.amount}"
    
    class Meta:
        unique_together = ['user', 'period', 'start_date']
        ordering = ['-start_date']


class SalesActivity(models.Model):
    """Sales activity tracking"""
    
    ACTIVITY_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('demo', 'Demo'),
        ('proposal', 'Proposal'),
        ('other', 'Other'),
    ]
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.activity_type}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Sales Activities"