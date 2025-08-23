from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.CompensationPlanListCreateView.as_view(), name='plan-list-create'),
    path('plans/<int:pk>/', views.CompensationPlanDetailView.as_view(), name='plan-detail'),
    path('user-plans/', views.UserCompensationPlanListCreateView.as_view(), name='user-plan-list-create'),
    path('commissions/', views.CommissionListView.as_view(), name='commission-list'),
    path('commissions/<int:pk>/', views.CommissionDetailView.as_view(), name='commission-detail'),
    path('payouts/', views.CommissionPayoutListCreateView.as_view(), name='payout-list-create'),
    path('calculate/', views.calculate_commissions, name='calculate-commissions'),
    path('summary/', views.commission_summary, name='commission-summary'),
    path('analytics/', views.commission_analytics, name='commission-analytics'),
    path('projections/', views.commission_projections, name='commission-projections'),
    path('trends/', views.commission_trends, name='commission-trends'),
]