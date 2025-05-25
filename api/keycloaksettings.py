import uuid
import logging
from typing import Dict
from django.conf import settings
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError

# Configura el logger para este módulo, lo que permite registrar información y errores.
logger = logging.getLogger(__name__)

class KeycloakIntegrationError(Exception):
    """
    Excepción personalizada para capturar y manejar errores durante la integración
    con el servicio de autenticación Keycloak.
    """
    pass  # No se requiere funcionalidad adicional, se utiliza solo para identificación de errores.

class KeycloakClient:
    """
    Cliente singleton para la integración con Keycloak.
    
    Este cliente se encarga de interactuar con el servicio de autenticación Keycloak,
    ofreciendo funcionalidades como la introspección de tokens, y centralizando el manejo
    de errores que se puedan presentar durante dicha interacción.
    """
    # Variable de clase para almacenar la instancia única del cliente.
    _instance = None

    def __new__(cls):
        """
        Implementa el patrón singleton, asegurando que solo se cree una instancia
        de KeycloakClient durante el ciclo de vida de la aplicación.
        
        Si la instancia aún no existe, se crea y se inicializa el cliente.
        En caso contrario, se retorna la instancia ya existente.
        """
        if cls._instance is None:
            cls._instance = super(KeycloakClient, cls).__new__(cls)
            # Inicializa el cliente con la configuración necesaria.
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        """
        Inicializa el cliente de Keycloak utilizando la configuración definida en
        settings.KEYCLOAK_CONFIG.
        
        Este método verifica que todos los parámetros necesarios (URL del servidor,
        realm, client id y client secret) estén presentes en la configuración. Si
        alguno falta, se lanza una excepción personalizada.
        
        Luego, se crea una instancia de KeycloakOpenID que se utiliza para interactuar
        con el servicio de Keycloak.
        """
        # Obtener la configuración de Keycloak desde los settings de Django.
        config = settings.KEYCLOAK_CONFIG
        
        # Definir los parámetros requeridos para la integración.
        required_config = ['SERVER_URL', 'REALM', 'CLIENT_ID', 'CLIENT_SECRET']
        
        # Verificar si falta algún parámetro esencial.
        missing = [key for key in required_config if key not in config]
        if missing:
            raise KeycloakIntegrationError(f"Incomplete Keycloak configuration. Missing: {missing}")
        
        # Crear la instancia del cliente de Keycloak con la configuración especificada.
        self.client = KeycloakOpenID(
            server_url=config['SERVER_URL'],
            realm_name=config['REALM'],
            client_id=config['CLIENT_ID'],
            client_secret_key=config['CLIENT_SECRET'],
            verify=not settings.DEBUG  # Desactiva la verificación de certificados en modo DEBUG.
        )

    def introspect_token(self, token: str) -> Dict:
        """
        Realiza la introspección del token JWT utilizando el cliente Keycloak.
        
        Este método se encarga de verificar la validez del token a través del método
        'introspect' del cliente Keycloak. En caso de producirse errores específicos de
        Keycloak o errores inesperados, estos son registrados y encapsulados en una
        excepción personalizada.
        
        Args:
            token (str): El token JWT que se desea validar e inspeccionar.
        
        Returns:
            Dict: Un diccionario con la información resultante de la introspección del token.
        
        Raises:
            KeycloakIntegrationError: Si ocurre un error durante la introspección del token.
        """
        try:
            # Intenta obtener la información del token a través de la introspección.
            return self.client.introspect(token)
        except KeycloakError as ke:
            # Registra errores conocidos de Keycloak y lanza una excepción personalizada.
            logger.error(f"Keycloak error during introspection: {str(ke)}", exc_info=True)
            raise KeycloakIntegrationError("Error communicating with authorization service") from ke
        except Exception as exc:
            # Registra cualquier otro error inesperado y lanza una excepción general.
            logger.critical(f"Unexpected error during introspection: {str(exc)}", exc_info=True)
            raise KeycloakIntegrationError("Unexpected error in authorization") from exc
