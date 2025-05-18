from rest_framework import viewsets
from .models import Cliente, Categoria, Marca, Producto, Talla, TallaProducto, Pedido, DetallePedido, Pago
from .serializers import (
    ClienteSerializer, CategoriaSerializer, MarcaSerializer, ProductoSerializer, 
    TallaSerializer, TallaProductoSerializer, TallaProductoCreateSerializer, PedidoSerializer, PedidoCreateSerializer, DetallePedidoSerializer, DetallePedidoCreateSerializer, 
    PagoSerializer, PagoCreateSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .auth import keycloak_protected
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from .permissions import KeycloakPermission

@swagger_auto_schema(method='get', operation_description="Obtener toda la información de productos, tallas, pedidos, etc.")
@keycloak_protected
@api_view(['GET'])
def allInfo(request):
    data = {
        "productos": ProductoSerializer(Producto.objects.all(), many=True).data,
        "tallas_producto": TallaProductoSerializer(TallaProducto.objects.all(), many=True).data,
        "pedidos": PedidoSerializer(Pedido.objects.all(), many=True).data,
        "detalles_pedido": DetallePedidoSerializer(DetallePedido.objects.all(), many=True).data,
        "clientes": ClienteSerializer(Cliente.objects.all(), many=True).data,
        "marcas": MarcaSerializer(Marca.objects.all(), many=True).data,
        "tallas": TallaSerializer(Talla.objects.all(), many=True).data
    }
    
    #Permission_classes = [IsAuthenticated]
    
    return JsonResponse(data, status=status.HTTP_200_OK)

# class ClienteViewSet(viewsets.ModelViewSet):
#     """
#     API endpoints para gestionar clientes
#     """
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer
    
#     @swagger_auto_schema(
#         operation_description="Lista todos los clientes",
#         responses={200: ClienteSerializer(many=True)}
#     )
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         operation_description="Crea un nuevo cliente",
#         request_body=ClienteSerializer,
#         responses={201: ClienteSerializer()}
#     )
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         operation_description="Obtiene detalles de un cliente específico",
#         responses={200: ClienteSerializer()}
#     )
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         operation_description="Actualiza un cliente existente",
#         request_body=ClienteSerializer,
#         responses={200: ClienteSerializer()}
#     )
#     def update(self, request, *args, **kwargs):
#         return super().update(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         operation_description="Actualiza parcialmente un cliente existente",
#         request_body=ClienteSerializer,
#         responses={200: ClienteSerializer()}
#     )
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         operation_description="Elimina un cliente",
#         responses={204: "No Content"}
#     )
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)

from functools import wraps
from django.http import JsonResponse
import requests
from jose import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .auth import keycloak_protected

# def keycloak_protected(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return JsonResponse({'error': 'No se proporcionó token de acceso'}, status=401)

#         token = auth_header.split('Bearer ')[1]

#         try:
#             introspect_url = f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
#             response = requests.post(
#                 introspect_url,
#                 data={'token': token, 'client_id': settings.KEYCLOAK_CLIENT_ID, 'client_secret': settings.KEYCLOAK_CLIENT_SECRET}
#             )

#             if response.status_code != 200:
#                 return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

#             return view_func(request, *args, **kwargs)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=401)
#     return _wrapped_view

@method_decorator(keycloak_protected, name='dispatch')
class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @swagger_auto_schema(
        operation_description="Lista todos los clientes",
        responses={200: ClienteSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo cliente",
        request_body=ClienteSerializer,
        responses={201: ClienteSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene detalles de un cliente específico",
        responses={200: ClienteSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza un cliente existente",
        request_body=ClienteSerializer,
        responses={200: ClienteSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un cliente existente",
        request_body=ClienteSerializer,
        responses={200: ClienteSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina un cliente",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# @method_decorator(keycloak_protected, name='dispatch')
class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar categorías de productos
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas las categorías",
        responses={200: CategoriaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva categoría",
        request_body=CategoriaSerializer,
        responses={201: CategoriaSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una categoría específica",
        responses={200: CategoriaSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una categoría existente",
        request_body=CategoriaSerializer,
        responses={200: CategoriaSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una categoría existente",
        request_body=CategoriaSerializer,
        responses={200: CategoriaSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una categoría",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# @method_decorator(keycloak_protected, name='dispatch')
class MarcaViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar marcas de productos
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas las marcas",
        responses={200: MarcaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva marca",
        request_body=MarcaSerializer,
        responses={201: MarcaSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una marca específica",
        responses={200: MarcaSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una marca existente",
        request_body=MarcaSerializer,
        responses={200: MarcaSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una marca existente",
        request_body=MarcaSerializer,
        responses={200: MarcaSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una marca",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# @method_decorator(keycloak_protected, name='dispatch')
class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar productos
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todos los productos disponibles",
        responses={200: ProductoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo producto",
        request_body=ProductoSerializer,
        responses={201: ProductoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de un producto específico",
        responses={200: ProductoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un producto existente",
        request_body=ProductoSerializer,
        responses={200: ProductoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un producto existente",
        request_body=ProductoSerializer,
        responses={200: ProductoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un producto",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Filtra productos por categoría",
        manual_parameters=[
            openapi.Parameter(
                'categoria', 
                openapi.IN_QUERY,
                description="ID de la categoría", 
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: ProductoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria')
        if categoria_id:
            productos = self.queryset.filter(categoria_id=categoria_id)
        else:
            productos = self.queryset.all()
        
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Filtra productos por marca",
        manual_parameters=[
            openapi.Parameter(
                'marca', 
                openapi.IN_QUERY,
                description="ID de la marca", 
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: ProductoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def por_marca(self, request):
        marca_id = request.query_params.get('marca')
        if marca_id:
            productos = self.queryset.filter(marca_id=marca_id)
        else:
            productos = self.queryset.all()
        
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

@method_decorator(keycloak_protected, name='dispatch')
class TallaViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar tallas
    """
    queryset = Talla.objects.all()
    serializer_class = TallaSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas las tallas",
        responses={200: TallaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva talla",
        request_body=TallaSerializer,
        responses={201: TallaSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una talla específica",
        responses={200: TallaSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una talla existente",
        request_body=TallaSerializer,
        responses={200: TallaSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una talla existente",
        request_body=TallaSerializer,
        responses={200: TallaSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una talla",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

@method_decorator(keycloak_protected, name='dispatch')
class TallaProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar relaciones entre tallas y productos
    """
    queryset = TallaProducto.objects.all()
    serializer_class = TallaProductoSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas las relaciones talla-producto",
        responses={200: TallaProductoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva relación talla-producto",
        request_body=TallaProductoCreateSerializer,
        responses={201: TallaProductoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una relación talla-producto específica",
        responses={200: TallaProductoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una relación talla-producto existente",
        request_body=TallaProductoCreateSerializer,
        responses={200: TallaProductoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una relación talla-producto existente",
        request_body=TallaProductoCreateSerializer,
        responses={200: TallaProductoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una relación talla-producto",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    # @swagger_auto_schema(
    #     operation_description="Filtra tallas disponibles por producto",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'producto', 
    #             openapi.IN_QUERY,
    #             description="ID del producto", 
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: TallaProductoSerializer(many=True)}
    # )
    # @action(detail=False, methods=['get'])
    # def por_producto(self, request):
    #     producto_id = request.query_params.get('producto')
    #     if producto_id:
    #         tallas_producto = self.queryset.filter(producto_id=producto_id)
    #     else:
    #         tallas_producto = self.queryset.all()
        
    #     serializer = self.get_serializer(tallas_producto, many=True)
    #     return Response(serializer.data)

@method_decorator(keycloak_protected, name='dispatch')
class PedidoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar pedidos
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todos los pedidos",
        responses={200: PedidoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo pedido",
        request_body=PedidoCreateSerializer,
        responses={201: PedidoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de un pedido específico",
        responses={200: PedidoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un pedido existente",
        request_body=PedidoCreateSerializer,
        responses={200: PedidoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un pedido existente",
        request_body=PedidoCreateSerializer,
        responses={200: PedidoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un pedido",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    # @swagger_auto_schema(
    #     operation_description="Filtra pedidos por cliente",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'cliente', 
    #             openapi.IN_QUERY,
    #             description="ID del cliente", 
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: PedidoSerializer(many=True)}
    # )
    # @action(detail=False, methods=['get'])
    # def por_cliente(self, request):
    #     cliente_id = request.query_params.get('cliente')
    #     if cliente_id:
    #         pedidos = self.queryset.filter(cliente_id=cliente_id)
    #     else:
    #         pedidos = self.queryset.all()
        
    #     serializer = self.get_serializer(pedidos, many=True)
    #     return Response(serializer.data)

@method_decorator(keycloak_protected, name='dispatch')
class DetallePedidoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar detalles de pedidos
    """
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todos los detalles de pedidos",
        responses={200: DetallePedidoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo detalle de pedido",
        request_body=DetallePedidoCreateSerializer,
        responses={201: DetallePedidoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene información de un detalle de pedido específico",
        responses={200: DetallePedidoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un detalle de pedido existente",
        request_body=DetallePedidoSerializer,
        responses={200: DetallePedidoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un detalle de pedido existente",
        request_body=DetallePedidoSerializer,
        responses={200: DetallePedidoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un detalle de pedido",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    # @swagger_auto_schema(
    #     operation_description="Filtra detalles por pedido",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'pedido', 
    #             openapi.IN_QUERY,
    #             description="ID del pedido", 
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: DetallePedidoSerializer(many=True)}
    # )
    # @action(detail=False, methods=['get'])
    # def por_pedido(self, request):
    #     pedido_id = request.query_params.get('pedido')
    #     if pedido_id:
    #         detalles = self.queryset.filter(pedido_id=pedido_id)
    #     else:
    #         detalles = self.queryset.all()
        
    #     serializer = self.get_serializer(detalles, many=True)
    #     return Response(serializer.data)

@method_decorator(keycloak_protected, name='dispatch')
class PagoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar pagos
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todos los pagos",
        responses={200: PagoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo pago",
        request_body=PagoCreateSerializer,
        responses={201: PagoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de un pago específico",
        responses={200: PagoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un pago existente",
        request_body=PagoSerializer,
        responses={200: PagoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un pago existente",
        request_body=PagoSerializer,
        responses={200: PagoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un pago",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Filtra pagos por pedido",
        manual_parameters=[
            openapi.Parameter(
                'pedido', 
                openapi.IN_QUERY,
                description="ID del pedido", 
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: PagoSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def por_pedido(self, request):
        pedido_id = request.query_params.get('pedido')
        if pedido_id:
            pagos = self.queryset.filter(pedido_id=pedido_id)
        else:
            pagos = self.queryset.all()
        
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)