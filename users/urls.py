from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.current_user_view, name='current-user'),
    path('teams/', views.SalesTeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', views.SalesTeamDetailView.as_view(), name='team-detail'),
]