from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Organization
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
        token['organization'] = user.organization.id if hasattr(user, 'organization') and user.organization else None
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra responses
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role.name if hasattr(self.user, 'role') and self.user.role else None,
                'organization': self.user.organization.id if hasattr(self.user, 'organization') and self.user.organization else None
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
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'organization')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Validate username
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        # Validate email
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        return data

    def create(self, validated_data):
        # Remove confirm_password from the data
        validated_data.pop('confirm_password', None)
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user

class JoinOrganizationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        if not Organization.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid organization code.")
        return value
