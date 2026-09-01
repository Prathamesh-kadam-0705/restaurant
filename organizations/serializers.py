from rest_framework import serializers

from organizations.models import Branch, Organization, OrganizationMembership

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization 
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at"
        )

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch 
        fields = (
            "id",
            "name",
            "address",
            "phone",
            "created_at",
            "updated_at"
        )

class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationMembership
        fields = (
            "id",
            "user",
            "organization",
            "role",
            "branch_access",
            "created_at",
            "updated_at"
        )