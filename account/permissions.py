from rest_framework.permissions import BasePermission

class HasSellerPermission(BasePermission):
    """
    Custom permission class to check if the user has seller permission.
    """

    def has_permission(self, request, view):
        # Check if the user's status is 'admin' 
        return request.user.status == 'admin' 