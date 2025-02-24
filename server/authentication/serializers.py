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
        if hasattr(obj, 'organization_id') and obj.organization_id:
            try:
                org = obj.organization
                if org:
                    # Format: "3 (3)" where first is ID and second is name
                    return f"{org.id} ({org.name})"
            except Organization.DoesNotExist:
                pass
        return None

    def get_role(self, obj):
        if hasattr(obj, 'role_id') and obj.role_id:
            try:
                role = obj.role
                if role:
                    # Return "Administrator" for admin role
                    return "Administrator" if role.name == "Admin" else role.get_name_display()
            except Role.DoesNotExist:
                pass
        return None

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    organization = OrganizationSerializer(read_only=True)  # Add organization to response

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'organization')
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
        password = validated_data.pop('password', None)
        
        # Create user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        
        return user

class JoinOrganizationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        if not Organization.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid organization code.")
        return value
