from rest_framework.views import APIView
from rest_framework.response import Response
from organizations.models import Branch, Organization, OrganizationMembership
from organizations.serializers import BranchSerializer, MembershipSerializer, OrganizationSerializer
from django.shortcuts import get_object_or_404

class OrganizationListCreateView(APIView):

    def post(self,request):

        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid() :
            organization = serializer.save()

            return Response(
                {
                    "massage":"Organization added successfully",
                    "organization":OrganizationSerializer(organization).data
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

class BranchListCreateView(APIView):

    def post(self,request,id):

        organization = get_object_or_404(Organization,id = id)

        serializer = BranchSerializer(data = request.data)

        if serializer.is_valid():

            branch = serializer.save(organization=organization)

            return Response(
                {
                    "message":"Branch added successfully",
                    "branch":BranchSerializer(branch).data
                },
                status=201
            )
        return Response(serializer.errors,400)

    def get(self,request,id):

        organization = get_object_or_404(Organization,id=id)

        branches = Branch.objects.filter(organization=organization)

        serializer = BranchSerializer(branches, many= True)

        return Response(serializer.data)

class MemberListCreateView(APIView):

    def post(self,request,id):

        organization = get_object_or_404(Organization,id=id)

        serializer = MembershipSerializer(data = request.data)

        if serializer.is_valid() :

            membership = serializer.save(organization=organization)

            return Response(
                {
                    "message": "Member added successfully",
                    "membership": MembershipSerializer(membership).data
                },
                status=201
            )

        return Response(serializer.errors,status=400)

    def get(self,request,id):

        organization = get_object_or_404(Organization,id=id)

        members = OrganizationMembership.objects.filter(organization=organization)

        serializer = MembershipSerializer(members,many = True)

        return Response(serializer.data)

class BranchDetailView(APIView):

    def get(self,request,id,branch_id):

        organization = get_object_or_404(Organization,id=id)
        branch = get_object_or_404(Branch,id=branch_id,organization=organization)
        serializer = BranchSerializer(branch)
        return Response(serializer.data)
