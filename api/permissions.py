# permissions.py
from rest_framework.permissions import BasePermission
from django.http import JsonResponse
import requests
from django.conf import settings

class KeycloakPermission(BasePermission):
    """
    Permiso personalizado que verifica el token JWT contra el servidor Keycloak.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split('Bearer ')[1]

        try:
            introspect_url = f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
            response = requests.post(
                introspect_url,
                data={
                    'token': token,
                    'client_id': settings.KEYCLOAK_CLIENT_ID,
                    'client_secret': settings.KEYCLOAK_CLIENT_SECRET
                }
            )

            if response.status_code != 200 or not response.json().get('active', False):
                return False

            return True  # Token válido
        except Exception:
            return False
