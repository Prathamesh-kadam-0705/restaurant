from rest_framework.views import APIView
from rest_framework.response import Response
from organizations.models import Branch, Category, Food, Organization, OrganizationMembership
from organizations.serializers import BranchSerializer, CategorySerializer, CategoryWithFoodsSerializer, FoodSerializer, MembershipSerializer, OrganizationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


from organizations.permissions import (
    IsOrganizationOwner,
    IsOrganizationMember,
    IsBranchManagerOrOwner,
)

class OrganizationListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid() :
            organization = serializer.save()

            OrganizationMembership.objects.create(
                user = request.user,
                organization=organization,
                role = 'OWNER',
            )

            return Response(
                {
                    "message":"Organization added successfully",
                    "organization":OrganizationSerializer(organization).data
                },
                status=201
            )
        return Response(serializer.errors,status=400)

    def get(self, request):
        organization_ids = OrganizationMembership.objects.filter(
            user=request.user
        ).values_list("organization_id", flat=True)

        organizations = Organization.objects.filter(
            id__in=organization_ids
        )

        serializer = OrganizationSerializer(
            organizations,
            many=True
        )

        return Response(serializer.data)

class OrganizationDetailView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsOrganizationMember()]

        return [IsAuthenticated(), IsOrganizationOwner()]

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

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOrganizationOwner()]

        return [IsAuthenticated(), IsOrganizationMember()]

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

    def get(self, request, id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        membership = OrganizationMembership.objects.get(
            user=request.user,
            organization=organization
        )

        if membership.role == "OWNER":
            branches = Branch.objects.filter(
                organization=organization
            )
        else:
            branches = membership.branch_access.filter(
                organization=organization
            )

        serializer = BranchSerializer(
            branches,
            many=True
        )

        return Response(serializer.data)

class MemberListCreateView(APIView):

    permission_classes = [IsAuthenticated, IsOrganizationOwner]

    def post(self,request,id):

        organization = get_object_or_404(Organization,id=id)

        serializer = MembershipSerializer(
            data=request.data,
            context={"organization": organization}
        )

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

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsOrganizationOwner()]

        return [IsAuthenticated(), IsBranchManagerOrOwner()]

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

    permission_classes = [IsAuthenticated, IsOrganizationOwner]
    
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
            partial = True,
            context={"organization": organization}
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

    def delete(self, request, id, member_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        member = get_object_or_404(
            OrganizationMembership,
            id=member_id,
            organization=organization
        )

        if member.user == request.user:
            return Response(
                {"error": "You cannot remove yourself from the organization."},
                status=400
            )

        if member.role == "OWNER":
            owner_count = OrganizationMembership.objects.filter(
                organization=organization,
                role="OWNER"
            ).count()

            if owner_count <= 1:
                return Response(
                    {
                        "error": "The organization must have at least one owner."
                    },
                    status=400
                )

        member.delete()

        return Response(status=204)
    
class FoodListCreateView(APIView):

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsBranchManagerOrOwner(),
        ]

    def post(self, request, id, branch_id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        serializer = FoodSerializer(
            data=request.data
        )

        if serializer.is_valid():

            category = serializer.validated_data["category"]

            if category.branch != branch:
                return Response(
                    {
                        "error": "Category does not belong to this branch."
                    },
                    status=400
                )

            food = serializer.save()

            return Response(
                {
                    "message": "Food added successfully",
                    "food": FoodSerializer(food).data
                },
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

    def get(self, request, id, branch_id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        foods = Food.objects.filter(
            category__branch=branch
        )

        serializer = FoodSerializer(
            foods,
            many=True
        )

        return Response(serializer.data)

class FoodDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsBranchManagerOrOwner,
    ]

    def get(self, request, id, branch_id, food_id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        food = get_object_or_404(
            Food,
            id=food_id,
            category__branch=branch
        )

        serializer = FoodSerializer(food)

        return Response(serializer.data)

    def patch(self, request, id, branch_id, food_id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        food = get_object_or_404(
            Food,
            id=food_id,
            category__branch=branch
        )

        serializer = FoodSerializer(
            food,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            category = serializer.validated_data.get("category")

            if category and category.branch != branch:
                return Response(
                    {
                        "error": "Category does not belong to this branch."
                    },
                    status=400
                )

            food = serializer.save()

            return Response(
                {
                    "message": "Food updated successfully",
                    "food": FoodSerializer(food).data
                },
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, id, branch_id, food_id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        food = get_object_or_404(
            Food,
            id=food_id,
            category__branch=branch
        )

        food.delete()

        return Response(status=204)

class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsBranchManagerOrOwner(),
            ]

        return [
            IsAuthenticated(),
            IsOrganizationMember(),
        ]

    def post(self, request, id, branch_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save(branch=branch)

            return Response(
                {
                    "message": "Category added successfully",
                    "category": CategorySerializer(category).data
                },
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

    def get(self, request, id, branch_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        categories = Category.objects.filter(
            branch=branch
        )

        serializer = CategoryWithFoodsSerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


class CategoryDetailView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsBranchManagerOrOwner,
    ]

    def get(self, request, id, branch_id, category_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        category = get_object_or_404(
            Category,
            id=category_id,
            branch=branch
        )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, id, branch_id, category_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        category = get_object_or_404(
            Category,
            id=category_id,
            branch=branch
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            category = serializer.save()

            return Response({
                "message": "Category updated successfully",
                "category": CategorySerializer(category).data
            })

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, id, branch_id, category_id):
        organization = get_object_or_404(
            Organization,
            id=id
        )

        branch = get_object_or_404(
            Branch,
            id=branch_id,
            organization=organization
        )

        category = get_object_or_404(
            Category,
            id=category_id,
            branch=branch
        )

        category.delete()

        return Response(status=204)