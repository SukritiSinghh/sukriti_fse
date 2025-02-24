from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer, 
    UserSerializer, 
    UserRegistrationSerializer
)

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get tokens from response
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            # Set JWT cookies
            response.set_cookie(
                'access_token',
                access_token,
                max_age=3600,  # 1 hour
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=86400,  # 1 day
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
        
        return response

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_permissions(self):
        if self.action == 'register':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        # Users can only see themselves and users in their organizations
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        
        # Get all users from organizations the current user belongs to
        user_orgs = user.organizations.all()
        return User.objects.filter(organizations__in=user_orgs).distinct()

    @action(detail=False, methods=['POST'])
    def register(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Get the user data with organization
            user_data = UserSerializer(user).data
            
            # Create response with tokens in cookies
            response = Response({
                'message': 'User created successfully',
                'user': user_data
            }, status=status.HTTP_201_CREATED)
            
            # Set JWT cookies
            response.set_cookie(
                'access_token',
                access_token,
                max_age=3600,  # 1 hour
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=86400,  # 1 day
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
            
            return response
            
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        try:
            # Get the refresh token from cookies
            refresh_token = request.COOKIES.get('refresh_token')
            
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                
            response = Response({"detail": "Successfully logged out."})
            # Delete the cookies
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            return response
        except Exception as e:
            return Response({"detail": "Error during logout."}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, 
        methods=['GET']
    )
    def me(self, request):
        try:
            # Get user directly from the database using the authenticated user's username
            user = User.objects.select_related('organization', 'role').get(username=request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
