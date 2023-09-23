from rest_framework import permissions

from api.tiers import TierResponseClass


class CanCreateAccountTierPermission(permissions.BasePermission):
    """
    Permissions class for check if the logged user is admin.
    """

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True

        return False


class CanRenewURLPermission(permissions.BasePermission):
    """
    Permission class for check if the user is a member of a account tier that gives a permission to renew a specific URL.
    """

    def has_permission(self, request, view):
        tier = TierResponseClass.get_tier(request.user)
        if tier.renew_url_perm:
            return True

        return False
