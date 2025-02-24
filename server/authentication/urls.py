from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView
)

from .views import (
    CustomTokenObtainPairView, 
    UserViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# Authentication URLs
auth_urls = [
    # JWT token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # User management endpoints
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
]

urlpatterns = [
    # Include authentication URLs
    path('', include(auth_urls)),
    
    # Include router URLs
    path('', include(router.urls)),
]
