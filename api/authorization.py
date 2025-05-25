import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import APIException
from rest_framework import status
import requests
import jwt  # Para decodificar el token sin necesidad de verificar la firma

logger = logging.getLogger(__name__)

class AuthorizationServiceException(APIException):
    """
    Excepción personalizada para errores relacionados con el servicio de autorización.
    
    Se utiliza para encapsular problemas de conexión, tiempo de espera o respuestas inesperadas
    provenientes del servicio de autorización (Keycloak).
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Authorization service unavailable'
    default_code = 'service_unavailable'

def check_keycloak_permission(token: str, permission: str) -> bool:
    """
    Verifica si el token JWT proporcionado posee el permiso solicitado utilizando dos estrategias:
    
      1. **Validación local:** Se decodifica el token (sin verificar la firma) y se revisa
         la sección "resource_access". Se espera que el permiso tenga el formato "<cliente>#<rol>".
         Si el rol requerido se encuentra en los roles asociados al cliente en el token, se
         aprueba la verificación.
      
      2. **Flujo UMA (fallback):** Si la validación local falla, se consulta el endpoint de Keycloak
         para solicitar un RPT (token de acceso) que confirme la concesión del permiso.
         Se cachea el resultado para evitar llamadas repetitivas.
    
    Args:
        token (str): Token JWT que se desea validar.
        permission (str): Permiso requerido para la acción solicitada, en formato "<cliente>#<rol>".
    
    Returns:
        bool: True si el permiso es concedido, False en caso contrario.
    
    Raises:
        AuthorizationServiceException: Para errores en la comunicación o respuesta inesperada
        del servicio de autorización.
    """
    try:
        # Primero: validación local de permisos
        try:
            # Decodificar el token sin verificar la firma para extraer los claims
            decoded = jwt.decode(token, options={"verify_signature": False})
        except Exception as exc:
            logger.error("Failed to decode token: %s", str(exc), exc_info=True)
            return False

        # Si el permiso viene en formato "<cliente>#<rol>", intentamos verificar localmente.
        if "#" in permission:
            resource_client, required_role = permission.split("#", 1)
            resource_access = decoded.get("resource_access", {})
            roles = resource_access.get(resource_client, {}).get("roles", [])
            if required_role in roles:
                logger.info("Permission '%s' found locally in token (resource '%s').", required_role, resource_client)
                return True
            else:
                logger.info("Permission '%s' not found locally in token for resource '%s'.", required_role, resource_client)
        else:
            # Si el permiso no tiene el formato esperado, se puede extender aquí otra lógica.
            logger.warning("Permission format not recognized: %s", permission)
        
        # Segundo: flujo UMA para validar el permiso en Keycloak (fallback)

        # Obtener la configuración de Keycloak desde los settings
        config = settings.KEYCLOAK_CONFIG
        if not all(config.get(key) for key in ('SERVER_URL', 'REALM', 'CLIENT_ID')):
            raise AuthorizationServiceException("Incomplete Keycloak configuration")
        
        client_id = config['CLIENT_ID']
        realm = config['REALM']
        server_url = config['SERVER_URL']
        if not server_url.endswith('/'):
            server_url += '/'
        
        # Generar una clave única para cachear el resultado de la verificación del permiso
        cache_key = f"keycloak_perm:{token}:{permission}"
        try:
            cached_result = cache.get(cache_key)
        except Exception as e:
            logger.error("Error accessing cache: %s", e)
            cached_result = None
        
        if cached_result is not None:
            return cached_result

        # Construir el endpoint del token en Keycloak para el flujo UMA
        token_endpoint = f"{server_url}realms/{realm}/protocol/openid-connect/token"
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": client_id,
            "permission": permission,
        }
        
        response = requests.post(token_endpoint, headers=headers, data=data, timeout=3)
        if response.status_code == 200:
            data_response = response.json()
            rpt = data_response.get("access_token")
            result = bool(rpt)
            if not result:
                logger.error("Token endpoint did not return an access_token for permission '%s'", permission)
        elif response.status_code in (400, 403):
            logger.info("Permission denied (status %s) from token endpoint for permission '%s'. Response: %s",
                        response.status_code, permission, response.text)
            result = False
        else:
            logger.error("Unexpected response from token endpoint: %s - %s", response.status_code, response.text)
            raise AuthorizationServiceException("Unexpected response from authorization service")
        
        # Guardar el resultado en cache para evitar llamadas repetidas (5 minutos)
        try:
            cache.set(cache_key, result, timeout=300)
        except Exception as e:
            logger.error("Error storing permission in cache: %s", e)
        except Exception () as e:
            logger.error('other cache error:',str(e))
        
        return result

    except requests.exceptions.Timeout:
        logger.warning("Timeout connecting to token endpoint")
        raise AuthorizationServiceException("Authorization service timeout")
    except requests.exceptions.RequestException as exc:
        logger.error("Connection error with token endpoint: %s", str(exc))
        raise AuthorizationServiceException("Authorization service connection error")
    except Exception as exc:
        logger.critical("Unexpected error: %s", str(exc), exc_info=True)
        raise AuthorizationServiceException("Unexpected error in authorization")
