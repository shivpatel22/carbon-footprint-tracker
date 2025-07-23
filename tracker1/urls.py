from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import HomeView

urlpatterns = [
    # path('', views.home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),

    # Django built-in login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('log/', views.log_activity, name='log_activity'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('team/', views.team_view, name='team'),
    path('charts/', views.chart_view, name='charts'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('edit-log/<int:log_id>/', views.edit_activity, name='edit_activity'),

    path('my-profile/', views.view_my_profile, name='view_my_profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='tracker1/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='tracker1/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tracker1/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='tracker1/password_reset_complete.html'), name='password_reset_complete'),
    path('set_goal/', views.set_goal, name='set_goal'),




]
