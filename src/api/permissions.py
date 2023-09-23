from rest_framework import permissions


class CanCreateAccountTierPermission(permissions.BasePermission):
    """
    Permissions classes for check if the logged user is admin. 
    """
   
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True 
        
        return False
