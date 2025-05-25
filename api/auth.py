from functools import wraps
from django.http import JsonResponse
import requests
from jose import jwt
from django.conf import settings

def keycloak_protected(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'No se proporcionó token de acceso'}, status=401)
        
        token = auth_header.split('Bearer ')[1]
        
        try:
            # Verificar el token con Keycloak
            introspect_url = f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
            response = requests.post(
                introspect_url,
                data={'token': token, 'client_id': settings.KEYCLOAK_CLIENT_ID, 'client_secret': settings.KEYCLOAK_CLIENT_SECRET}
            )
            
            if response.status_code != 200 or not response.json().get('active', False):

                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)
                #return JsonResponse({'debug': response.json()}, status=200)
                
                #return JsonResponse({'codigo': response.status_code, 'active': response.json().get('active', False),'error': 'Token inválido o expirado'}, status=401)                           
                
            # Si llegamos aquí, el token es válido
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
    
    return _wrapped_view