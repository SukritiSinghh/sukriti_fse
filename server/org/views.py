from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.models import Organization, Role
from authentication.serializers import OrganizationSerializer, JoinOrganizationSerializer

# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'join_organization']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def create_organization(self, request):
        """Allows a user to create an organization and become its Admin."""
        serializer = OrganizationSerializer(data=request.data)
        
        if serializer.is_valid():
            organization = serializer.save()
            user = request.user
            user.organization = organization
            admin_role, _ = Role.objects.get_or_create(name='Admin')  # Assign Admin Role
            user.role = admin_role
            user.save()

            return Response({
                "message": "Organization created successfully",
                "organization_id": organization.id,
                "organization_name": organization.name,
                "admin": user.username
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def join_organization(self, request):
        """Allows a user to join an existing organization using an invite code."""
        serializer = JoinOrganizationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            organization_code = serializer.validated_data['code']
            organization = get_object_or_404(Organization, code=organization_code)

            user = request.user
            if user.organization:
                return Response({"error": "User is already part of an organization"}, status=status.HTTP_400_BAD_REQUEST)

            user.organization = organization
            admin_role, _ = Role.objects.get_or_create(name='Admin')  # Assign Admin Role
            user.role = admin_role
            user.save()

            return Response({
                "message": "Successfully joined organization",
                "organization_id": organization.id,
                "organization_name": organization.name
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
