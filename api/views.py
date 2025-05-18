from .models import Cliente, Categoria, Marca, Talla, Color, Producto, ProductoTallaColor, Pedido, DetallePedido, Pago
from rest_framework import viewsets

from .serializers import (
    ClienteSerializer, 
    CategoriaSerializer, 
    MarcaSerializer, 
    TallaSerializer, 
    ColorSerializer, 
    ProductoSerializer, 
    ProductoTallaColorSerializer, 
    ProductoTallaColorCreateSerializer,
    PedidoSerializer, 
    PedidoCreateSerializer, 
    DetallePedidoSerializer, 
    DetallePedidoCreateSerializer, 
    PagoSerializer, 
    PagoCreateSerializer
)

from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import KeycloakPermission
from django.http import JsonResponse
from .auth import keycloak_protected
from rest_framework import status
from drf_yasg import openapi

from rest_framework import viewsets
from django.conf import settings
from .models import Cliente
from functools import wraps
from jose import jwt
import requests

# API View para obtener toda la información
@swagger_auto_schema(method='get', operation_description="Obtener toda la información de productos, tallas, pedidos, etc.")
#@keycloak_protected
@api_view(['GET'])
def allInfo(request):
    data = {
        "clientes": ClienteSerializer(Cliente.objects.all(), many=True).data,
        "categorias": CategoriaSerializer(Categoria.objects.all(), many=True).data,
        "marcas": MarcaSerializer(Marca.objects.all(), many=True).data,
        "tallas": TallaSerializer(Talla.objects.all(), many=True).data,
        "colores": ColorSerializer(Color.objects.all(), many=True).data,
        "productos": ProductoSerializer(Producto.objects.all(), many=True).data,
        "productos_talla_color": ProductoTallaColorSerializer(ProductoTallaColor.objects.all(), many=True).data,
        "pedidos": PedidoSerializer(Pedido.objects.all(), many=True).data,
        "detalles_pedido": DetallePedidoSerializer(DetallePedido.objects.all(), many=True).data,
        "pagos": PagoSerializer(Pago.objects.all(), many=True).data
    }
    
    return JsonResponse(data, status=status.HTTP_200_OK)

#@method_decorator(keycloak_protected, name='dispatch')
class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    #permission_classes = [IsAuthenticated, KeycloakPermission]

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

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar categorias
    """
    
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    #permission_classes = [IsAuthenticated, KeycloakPermission]

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

class MarcaViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar marcas
    """
    
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    #permission_classes = [IsAuthenticated, KeycloakPermission]

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

class ColorViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar colores
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas los colores",
        responses={200: ColorSerializer(many=True)}
    )
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea un nuevo color",
        request_body=ColorSerializer,
        responses={201: ColorSerializer()}
    )
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de un color específico",
        responses={200: ColorSerializer()}
    )
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un color existente",
        request_body=ColorSerializer,
        responses={200: ColorSerializer()}
    )
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un color existente",
        request_body=ColorSerializer,
        responses={200: ColorSerializer()}
    )
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un color",
        responses={204: "No Content"}
    )
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar productos
    """
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    #permission_classes = [IsAuthenticated, KeycloakPermission]

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
        operation_description="Filtra productos por categoría",
        manual_parameters=[openapi.Parameter('categoria', openapi.IN_QUERY, description="ID de la categoría", type=openapi.TYPE_INTEGER)],
        responses={200: ProductoSerializer(many=True)}
    )
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria')
        productos = self.queryset.filter(categoria_id=categoria_id) if categoria_id else self.queryset.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Filtra productos por marca",
        manual_parameters=[openapi.Parameter('marca', openapi.IN_QUERY, description="ID de la marca", type=openapi.TYPE_INTEGER)],
        responses={200: ProductoSerializer(many=True)}
    )
    
    @action(detail=False, methods=['get'])
    def por_marca(self, request):
        marca_id = request.query_params.get('marca')
        productos = self.queryset.filter(marca_id=marca_id) if marca_id else self.queryset.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class ProductoTallaColorViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar relaciones entre productos, tallas y colores
    """
    queryset = ProductoTallaColor.objects.all()
    serializer_class = ProductoTallaColorSerializer
    
    @swagger_auto_schema(
        operation_description="Lista todas las relaciones producto-talla-color",
        responses={200: ProductoTallaColorSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva relación producto-talla-color",
        request_body=ProductoTallaColorCreateSerializer,
        responses={201: ProductoTallaColorSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una relación producto-talla-color específica",
        responses={200: ProductoTallaColorSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una relación producto-talla-color existente",
        request_body=ProductoTallaColorCreateSerializer,
        responses={200: ProductoTallaColorSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una relación producto-talla-color existente",
        request_body=ProductoTallaColorCreateSerializer,
        responses={200: ProductoTallaColorSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una relación producto-talla-color",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#@method_decorator(keycloak_protected, name='dispatch')
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
        request_body=PedidoSerializer,
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
        request_body=PedidoSerializer,
        responses={200: PedidoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un pedido existente",
        request_body=PedidoSerializer,
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
#@method_decorator(keycloak_protected, name='dispatch')
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

#@method_decorator(keycloak_protected, name='dispatch')
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
        request_body=PagoSerializer,
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
        operation_description="Elimina un pago",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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