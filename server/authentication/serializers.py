from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Organization, Role
import logging

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['id'] = user.id
        
        # Add role and organization if they exist
        token['role'] = user.role.name if hasattr(user, 'role') and user.role else None
        if hasattr(user, 'organization') and user.organization:
            token['organization'] = {
                'id': user.organization.id,
                'name': user.organization.name,
                'code': user.organization.code
            }
        else:
            token['organization'] = None
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra responses with full organization details
        organization_data = None
        if hasattr(self.user, 'organization') and self.user.organization:
            organization_data = {
                'id': self.user.organization.id,
                'name': self.user.organization.name,
                'code': self.user.organization.code
            }
        
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role.name if hasattr(self.user, 'role') and self.user.role else None,
                'organization': organization_data
            }
        })
        
        return data

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'code', 'address']

    def create(self, validated_data):
        # Generate a unique code if not provided
        if 'code' not in validated_data:
            import uuid
            validated_data['code'] = str(uuid.uuid4())[:8].upper()
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    staff_status = serializers.BooleanField(source='is_staff', read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'organization', 'role', 'staff_status']

    def get_organization(self, obj):
        if hasattr(obj, 'organization') and obj.organization:
            return {
                'id': obj.organization.id,
                'name': obj.organization.name,
                'code': obj.organization.code
            }
        return None

    def get_role(self, obj):
        if hasattr(obj, 'role') and obj.role:
            return obj.role.name
        return None

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'organization', 'role')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check if username exists
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        # Check if email exists
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            **{k: v for k, v in validated_data.items() if k not in ['username', 'email']}
        )
        return user

class JoinOrganizationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        if not Organization.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid organization code.")
        return value
