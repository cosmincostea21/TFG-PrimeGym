from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
]
