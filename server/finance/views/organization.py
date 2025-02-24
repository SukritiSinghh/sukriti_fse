from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Organization
from ..serializers import OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new organization and assign the creator as a member"""
        organization = serializer.save()
        self.request.user.organization = organization
        self.request.user.save()

    @action(detail=False, methods=['post'])
    def join(self, request):
        """Join an existing organization using its code"""
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'Organization code is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organization = Organization.objects.get(code=code)
            request.user.organization = organization
            request.user.save()
            return Response(
                OrganizationSerializer(organization).data,
                status=status.HTTP_200_OK
            )
        except Organization.DoesNotExist:
            return Response(
                {'error': 'Invalid organization code'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the current user's organization"""
        if request.user.organization:
            return Response(
                OrganizationSerializer(request.user.organization).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'User is not part of any organization'},
            status=status.HTTP_404_NOT_FOUND
        )
