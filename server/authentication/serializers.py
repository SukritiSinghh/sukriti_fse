from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Organization

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'address', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), 
        source='organization', 
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'organization', 'organization_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Only allow Admin to create users
        current_user = self.context.get('request').user
        if current_user.role != 'Admin':
            raise serializers.ValidationError("Only Admin can create users")
        
        # Remove organization from validated_data if not provided
        organization = validated_data.pop('organization', None)
        
        # Create user
        user = User.objects.create(**validated_data)
        
        # Set organization if provided
        if organization:
            user.organization = organization
            user.save()
        
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'organization']
        extra_kwargs = {
            'password': {'write_only': True},
            'organization': {'required': False}
        }

    def validate(self, data):
        # Validate password match
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        
        # Only Admin can create users with Admin role
        current_user = self.context.get('request').user
        if data.get('role') == 'Admin' and (not current_user or current_user.role != 'Admin'):
            raise serializers.ValidationError("Only existing Admin can create Admin users")
        
        return data

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role'],
            organization=validated_data.get('organization')
        )
        return user
