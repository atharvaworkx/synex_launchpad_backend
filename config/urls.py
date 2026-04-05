"""
URL configuration for Synex Innovations project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({'status': 'ok', 'message': 'Backend is running'})

def email_config_check(request):
    """Check email configuration"""
    return JsonResponse({
        'EMAIL_HOST': settings.EMAIL_HOST,
        'EMAIL_PORT': settings.EMAIL_PORT,
        'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD': '***' + settings.EMAIL_HOST_PASSWORD[-4:] if settings.EMAIL_HOST_PASSWORD else 'NOT SET',
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'CONTACT_EMAIL_TO': settings.CONTACT_EMAIL_TO,
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contact/', include('contact.urls')),
    path('health/', health_check, name='health_check'),
    path('email-config/', email_config_check, name='email_config_check'),
]
