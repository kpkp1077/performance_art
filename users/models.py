from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model for QuotaPath"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Sales Manager'),
        ('rep', 'Sales Representative'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='rep')
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField(blank=True, null=True)
    is_active_sales = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class SalesTeam(models.Model):
    """Sales team model"""
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name