from rest_framework.permissions import BasePermission, SAFE_METHODS

class PublicGetAdminWritePermission(BasePermission):
    """
    - Permite GET público sin autenticación.
    - Requiere autenticación y rol 'administrator' para otros métodos.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False
        if not hasattr(user, 'roles'):
            return False
        return 'administrator' in user.roles
