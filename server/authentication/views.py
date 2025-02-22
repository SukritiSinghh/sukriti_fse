from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Organization
from .serializers import (
    CustomTokenObtainPairSerializer, 
    UserSerializer, 
    UserRegistrationSerializer,
    OrganizationSerializer
)

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        # Admin sees all users, others see only their own
        user = self.request.user
        if user.role == 'Admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request):
        # Only Admin can register new users
        if request.user.role != 'Admin':
            return Response(
                {"error": "Only Admin can register new users"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserRegistrationSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user_id": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin sees all organizations, others see only their own
        user = self.request.user
        if user.role == 'Admin':
            return Organization.objects.all()
        return Organization.objects.filter(id=user.organization_id)

# Custom permission class for role-based access
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'

class IsFinanceUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['Admin', 'Finance']
