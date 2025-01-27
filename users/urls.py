from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('registro/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.profile, name='perfil'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/usuarios/perfil/'
    ), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('staff/', views.staff_home, name='staff_home'),
    path('staff/register/', views.staff_register, name='staff_register'),
]