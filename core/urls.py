from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('users/<pk>/', views.user_detail, name='user_detail'),    path('user/<pk>/update/', views.user_update, name='user_update'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('get-sub-departments/<int:department_id>/', views.get_sub_departments, name='get_sub_departments'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<pk>/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('Game-leaderboard/', views.update_user_score, name='leaderboard1'),
    path('help/', views.help, name='help'),
    
    # Add redirects for common auth URLs
    path('accounts/login/', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('accounts/profile/', RedirectView.as_view(pattern_name='dashboard', permanent=True)),
    re_path(r'^accounts/.*$', RedirectView.as_view(pattern_name='login', permanent=True)),
]
