"""
URL configuration for insuretech project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include([
        # Authentication routes
        path('auth/', include('authentication.urls')),
        
        # Organization routes
        path('org/', include('org.urls')),
        
        # Finance routes
        path('finance/', include('finance.urls')),
    ])),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
