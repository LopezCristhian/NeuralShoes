import jwt
from jwt import PyJWKClient
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.core.cache import cache
import logging
import redis
from django_redis.exceptions import ConnectionInterrupted

# Configuración del logger para registrar eventos y errores en el módulo actual.
logger = logging.getLogger(__name__)

class KeycloakAuthentication(BaseAuthentication):
    """
    Clase de autenticación personalizada para validar tokens JWT emitidos por Keycloak.
    
    Este autenticador procesa el encabezado de autorización, decodifica el token JWT, 
    verifica su firma y su contenido, y utiliza la introspección de Keycloak para confirmar
    la validez del token. Además, implementa caching para optimizar la verificación.
    """
    
    def authenticate(self, request):
        """
        Procesa la solicitud para extraer y validar el token JWT.
        
        Se extrae el token del encabezado 'Authorization', se valida el formato, y se decodifica
        utilizando la clave pública obtenida del endpoint JWKS de Keycloak. Luego, se verifica que 
        el token contenga los claims esperados ('azp' o 'aud') que confirmen la identidad del cliente.
        Se utiliza la introspección para comprobar que el token esté activo y no haya expirado.
        
        Args:
            request: Objeto de la solicitud HTTP.
        
        Returns:
            Tuple: Una tupla (user, token) en caso de autenticación exitosa.
        
        Raises:
            AuthenticationFailed: Si el token es inválido, mal formado o no cumple con los requisitos.
        """
        # Extraer el encabezado 'Authorization' de la solicitud
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            # No se proporciona token, se retorna None para permitir otros métodos de autenticación
            return None
        
        # Separar el esquema del token; se espera el formato "Bearer <token>"
        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise AuthenticationFailed('Invalid Authorization header. Expected "Bearer <token>".')
        
        # Extraer el token JWT del encabezado
        token = parts[1]

        try:
            # Obtener la configuración de Keycloak desde los settings de Django
            config = settings.KEYCLOAK_CONFIG
            realm = config['REALM']
            server_url = config['SERVER_URL']
            
            # Asegurar que la URL del servidor finalice con una barra "/"
            if not server_url.endswith('/'):
                server_url += '/'
            
            # Construir la URL para obtener las claves públicas (JWKS) de Keycloak
            jwks_url = f"{server_url}realms/{realm}/protocol/openid-connect/certs"
            
            # Instanciar el cliente para obtener la clave de firma del token
            jwk_client = PyJWKClient(jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)
            
            # Establecer el issuer esperado basado en la configuración de Keycloak
            issuer = f"{server_url}realms/{realm}"
            
            # Decodificar el token JWT utilizando la clave de firma obtenida y los parámetros de validación
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=issuer,
                options={"verify_exp": True, "verify_aud": False}  # La validación de 'aud' se maneja manualmente
            )
            
            # Verificar que el token contenga el claim 'azp' o 'aud' con el valor esperado del cliente
            client_id = config['CLIENT_ID']
            azp = decoded.get("azp")
            aud = decoded.get("aud")
            valid = False
            if azp == client_id:
                valid = True
            elif isinstance(aud, list) and client_id in aud:
                valid = True
            elif aud == client_id:
                valid = True

            if not valid:
                # Si ninguno de los claims coincide con el client_id, se rechaza el token
                raise AuthenticationFailed("Invalid token: Neither 'azp' nor 'aud' contains expected client")
            
            # Construir una clave para cachear la introspección del token
            cache_key = f"keycloak_token_introspect:{token}"
            introspection = None
            
            try:
                # Intentar recuperar el resultado de la introspección desde el cache
                introspection = cache.get(cache_key)
            except (ConnectionInterrupted, redis.exceptions.TimeoutError) as e:
                logger.error("Cache error on get: %s", str(e))
                introspection = None

            if introspection is None:
                # Importación local para evitar dependencias circulares
                from api.keycloaksettings import KeycloakClient  
                # Realizar la introspección del token utilizando el cliente de Keycloak
                introspection = KeycloakClient().introspect_token(token)
                try:
                    # Guardar el resultado de la introspección en el cache por 300 segundos
                    cache.set(cache_key, introspection, timeout=300)
                except (ConnectionInterrupted, redis.exceptions.TimeoutError) as e:
                    logger.error("Cache error on set: %s", str(e))
            
            # Comprobar que la respuesta de introspección indique que el token está activo
            if not introspection.get('active', False):
                raise AuthenticationFailed("Token is inactive or expired")
            
        except Exception as exc:
            # En caso de cualquier error durante el proceso de autenticación, se rechaza el token
            raise AuthenticationFailed(f"Invalid token: {str(exc)}")
        
        # Obtener o crear el usuario correspondiente al token decodificado
        user = self.get_or_create_user(decoded)
        # Retornar el usuario autenticado junto con el token utilizado
        return (user, token)

    def get_or_create_user(self, decoded_token):
        """
        Recupera o crea un usuario basado en la información contenida en el token decodificado.
        
        Se utiliza el claim 'preferred_username' o 'sub' para identificar de forma única al usuario.
        Si el usuario no existe en la base de datos, se crea uno nuevo con una contraseña inutilizable.
        
        Args:
            decoded_token (dict): Diccionario con los claims decodificados del token.
        
        Returns:
            User: Instancia del modelo de usuario de Django.
        
        Raises:
            AuthenticationFailed: Si el token no contiene un identificador de usuario válido.
        """
        from django.contrib.auth.models import User
        
        # Extraer el nombre de usuario preferido o utilizar el identificador 'sub' como respaldo
        username = decoded_token.get('preferred_username') or decoded_token.get('sub')
        if not username:
            raise AuthenticationFailed("Token does not contain a valid user identifier.")
        
        # Buscar el usuario en la base de datos; si no existe, se crea uno nuevo
        user, created = User.objects.get_or_create(username=username)
        if created:
            # Si se crea un nuevo usuario, se establece una contraseña inutilizable
            user.set_unusable_password()
            user.save()
        return user
