from rest_framework.permissions import BasePermission, SAFE_METHODS

class HasKeycloakRole(BasePermission):
    """
    Permite acceso basado en roles del token JWT de Keycloak.
    """
    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'roles'):
            return False
        
        # if request.method in SAFE_METHODS:
        #     return 'client' in user.roles or 'administrator' in user.roles
        # elif request.method in ['POST', 'DELETE']:
        #     return 'administrator' in user.roles
        # elif request.method in ['PUT', 'PATCH']:
        #     return 'client' in user.roles or 'administrator' in user.roles
        # else:
        #     return False

        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return 'client' in user.roles or 'administrator' in user.roles
        else:  # POST, PUT, PATCH, DELETE
            return 'administrator' in user.roles
