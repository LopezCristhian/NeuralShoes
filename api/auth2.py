# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from jwt.exceptions import InvalidTokenError

class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        # Clave pública de Keycloak en formato PEM
        public_key = settings.KEYCLOAK_CONFIG['KEYCLOAK_PUBLIC_KEY']
        # Keycloak usualmente da la clave pública sin encabezados PEM,
        # así que asegurarse de que esté en el formato correcto:
        if not public_key.startswith('-----BEGIN PUBLIC KEY-----'):
            public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

        try:
            token_info = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options={"verify_aud": False}  # Puedes activar verify_aud si quieres
            )
        except InvalidTokenError as e:
            raise AuthenticationFailed(f'Token inválido o expirado: {str(e)}')

        username = token_info.get("preferred_username")
        roles = token_info.get("realm_access", {}).get("roles", [])

        # Usuario simple con info útil
        class SimpleUser:
            def __init__(self, username, roles, token_info):
                self.username = username
                self.roles = roles
                self.token_info = token_info

            @property
            def is_authenticated(self):
                return True

        user = SimpleUser(username, roles, token_info)
        return (user, None)
