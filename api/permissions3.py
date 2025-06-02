from rest_framework.permissions import BasePermission, SAFE_METHODS

class HasKeycloakRoleClient(BasePermission):
    """
    Permite acceso basado en roles del token JWT de Keycloak.
    """
    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'roles'):
            return False

        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return 'client' in user.roles or 'administrator' in user.roles
        else:  # POST, PUT, PATCH, DELETE
            return 'client' in user.roles
