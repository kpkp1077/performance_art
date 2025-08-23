from django.urls import path
from . import views

urlpatterns = [
    path('deals/', views.DealListCreateView.as_view(), name='deal-list-create'),
    path('deals/<int:pk>/', views.DealDetailView.as_view(), name='deal-detail'),
    path('quotas/', views.QuotaListCreateView.as_view(), name='quota-list-create'),
    path('quotas/<int:pk>/', views.QuotaDetailView.as_view(), name='quota-detail'),
    path('activities/', views.SalesActivityListCreateView.as_view(), name='activity-list-create'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
    path('pipeline-analysis/', views.pipeline_analysis, name='pipeline-analysis'),
    path('quota-performance/', views.quota_performance, name='quota-performance'),
]