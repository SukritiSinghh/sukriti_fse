from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
