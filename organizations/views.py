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
                    "message":"Organization added successfully",
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

    def patch(self,request,id):

        organization = get_object_or_404(Organization,id=id)
        serializer = OrganizationSerializer(organization,data = request.data,partial = True)

        if serializer.is_valid() :
            serializer.save()

            return Response(
                {
                    "message":"Organization updated successfully",
                    "organization":OrganizationSerializer(organization).data
                },
                status=200
            )
        return Response(serializer.errors,status=400)

    def delete(self,request,id):

        organization = get_object_or_404(Organization,id=id)
        organization.delete()

        return Response(status=204)

class BranchListCreateView(APIView):

    def post(self, request, id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        serializer = MembershipSerializer(
            data=request.data,
            context={"organization": organization}
        )

        if serializer.is_valid():

            membership = serializer.save(
                organization=organization
            )

            return Response(
                {
                    "message": "Member added successfully",
                    "membership": MembershipSerializer(membership).data
                },
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

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

    def patch(self,request,id,branch_id):

        organization = get_object_or_404(Organization,id=id)
        branch = get_object_or_404(Branch,id=branch_id,organization=organization)
        serializer = BranchSerializer(
            branch,
            data=request.data,
            partial = True
        )

        if serializer.is_valid() :
            branch = serializer.save()

            return Response(
                {
                    "message": "Branch updated successfully",
                    "branch":BranchSerializer(branch).data
                },
                status=200
            )
        
        return Response(serializer.errors,status=400)

    def delete(self,request,id,branch_id):

        organization = get_object_or_404(Organization,id=id)
        branch = get_object_or_404(Branch,id=branch_id,organization=organization)
        branch.delete()

        return Response(
            status=204
        )


class MemberDetailView(APIView):

    def get(self,request,id,member_id):

        organization = get_object_or_404(Organization,id=id)
        member = get_object_or_404(OrganizationMembership,id= member_id,organization=organization)
        serializer = MembershipSerializer(member)
        return Response(serializer.data)

    def patch(self,request,id,member_id):
        organization = get_object_or_404(Organization,id=id)
        member = get_object_or_404(OrganizationMembership,id=member_id,organization=organization)
        serializer = MembershipSerializer(
            member,
            data = request.data,
            partial = True
        )

        if serializer.is_valid() :
            member = serializer.save()

            return Response(
                {
                    "message":"Member updated successfully",
                    "member":MembershipSerializer(member).data
                },
                status=200
            )
        return Response(serializer.errors,status=400)

    def delete(self,request,id,member_id):

        organization = get_object_or_404(Organization,id=id)
        member = get_object_or_404(OrganizationMembership,id=member_id,organization=organization)
        member.delete()
        return Response(status=204)
