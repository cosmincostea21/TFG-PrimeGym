from django.urls import path, include
from django.contrib.auth import views as auth_views  # Falta esta importación
from . import views

urlpatterns = [
    # 1. Rutas de recuperación de contraseña (DEBEN ir antes del include genérico)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # 2. Tu ruta de registro
    path('accounts/register/', views.register, name='register'),

    # 3. Rutas automáticas de Django (login, logout, etc.)
    path('account/', include('django.contrib.auth.urls')),
]
