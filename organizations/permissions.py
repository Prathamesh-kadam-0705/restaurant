from rest_framework.permissions import BasePermission

from organizations.models import OrganizationMembership


class IsOrganizationOwner(BasePermission):
    """
    Allows only the organization owner.
    """

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("id")

        if not organization_id:
            return False

        return OrganizationMembership.objects.filter(
            user=request.user,
            organization_id=organization_id,
            role="OWNER",
        ).exists()


class IsOrganizationMember(BasePermission):
    """
    Allows users who belong to the organization.
    """

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("id")

        if not organization_id:
            return False

        return OrganizationMembership.objects.filter(
            user=request.user,
            organization_id=organization_id,
        ).exists()


class IsBranchManagerOrOwner(BasePermission):
    """
    OWNER can access all branches.
    MANAGER can access only assigned branches.
    """

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("id")
        branch_id = view.kwargs.get("branch_id")

        if not organization_id or not branch_id:
            return False

        membership = OrganizationMembership.objects.filter(
            user=request.user,
            organization_id=organization_id,
        ).first()

        if not membership:
            return False

        if membership.role == "OWNER":
            return True

        if membership.role == "MANAGER":
            return membership.branch_access.filter(
                id=branch_id,
                organization_id=organization_id,
            ).exists()

        return False