from rest_framework import serializers

from organizations.models import Branch, Category, Food, Organization, OrganizationMembership

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
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = OrganizationMembership
        fields = (
            "id",
            "email",
            "user",
            "organization",
            "role",
            "branch_access",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "organization",
            "created_at",
            "updated_at",
        )

    def validate_email(self, email):
        from accounts.models import User

        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user exists with this email."
            )

    def validate_branch_access(self, branches):
        organization = self.context.get("organization")

        if not organization:
            raise serializers.ValidationError(
                "Organization is required."
            )

        for branch in branches:
            if branch.organization != organization:
                raise serializers.ValidationError(
                    "You cannot assign branches from another organization."
                )

        return branches

   
    def create(self, validated_data):
        user = validated_data.pop("email")
        organization = validated_data.pop("organization")

        if OrganizationMembership.objects.filter(
            user=user,
            organization=organization
        ).exists():
            raise serializers.ValidationError(
                "User is already a member of this organization."
            )

        return OrganizationMembership.objects.create(
            user=user,
            organization=organization,
            **validated_data
        )
    def validate(self, data):
    # Email is required when creating a member
        if not self.instance and "email" not in data:
            raise serializers.ValidationError({
                "email": "Email is required when adding a member."
            })

        role = data.get(
            "role",
            self.instance.role if self.instance else None
        )

        branches = data.get(
            "branch_access",
            self.instance.branch_access.all()
            if self.instance else []
        )

        if role == "MANAGER" and not branches:
            raise serializers.ValidationError({
                "branch_access": "A manager must have at least one branch."
            })

        if role == "OWNER" and branches:
            raise serializers.ValidationError({
                "branch_access": "An owner should not have branch assignments."
            })

        # Prevent removing the last owner
        if (
            self.instance
            and self.instance.role == "OWNER"
            and role != "OWNER"
        ):
            owner_count = OrganizationMembership.objects.filter(
                organization=self.instance.organization,
                role="OWNER"
            ).count()

            if owner_count <= 1:
                raise serializers.ValidationError({
                    "role": "The organization must have at least one owner."
                })

        return data

class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = (
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",
            "is_available",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "branch",
            "name",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "branch",
            "created_at",
            "updated_at",
        )

class CategoryWithFoodsSerializer(serializers.ModelSerializer):

    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "branch",
            "name",
            "description",
            "foods",
            "created_at",
            "updated_at",
        )