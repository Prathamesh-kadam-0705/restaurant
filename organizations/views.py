from rest_framework.views import APIView
from rest_framework.response import Response
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer
from django.shortcuts import get_object_or_404

class OrganizationListCreateView(APIView):

    def post(self,request):

        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid() :
            organization = serializer.save()

            return Response(
                {
                    "massage":"Organization added successfully",
                    "organiztion":OrganizationSerializer(organization).data
                },
                status=201
            )
        return Response(serializer.errors,status=400)

    def get(self,request):

        organizations = Organization.objects.all()

        serializer = OrganizationSerializer(organizations, many = True)

        return Response(serializer.data)

class OrganizationDetailView(APIView):

    def get(self,request,id):

        organization = get_object_or_404(
            Organization,
            id=id        
        )

        serializer = OrganizationSerializer(organization)

        return Response(serializer.data)

