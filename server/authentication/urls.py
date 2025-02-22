from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

from .views import (
    CustomTokenObtainPairView, 
    UserViewSet, 
    OrganizationViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    # Authentication URLs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # User registration and management
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),
    
    # Include router URLs
    path('', include(router.urls)),
]
