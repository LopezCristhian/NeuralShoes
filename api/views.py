from api.authentication import KeycloakAuthentication
from .models import Cliente, Categoria, Marca, Talla, Color, Producto, ProductoImagen, ProductoTallaColor, Carrito, ItemCarrito, Pedido, DetallePedido, Pago
from rest_framework import viewsets
#from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ClienteSerializer, 
    CategoriaSerializer, 
    MarcaSerializer, 
    TallaSerializer, 
    ColorSerializer, 
    ProductoSerializer, 
    ProductoImagenSerializer,
    ProductoTallaColorSerializer, 
    ProductoTallaColorCreateSerializer,
    PedidoSerializer, 
    CarritoSerializer,
    ItemCarritoCreateSerializer,
    ItemCarritoSerializer,
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


from .models import agregar_o_actualizar_item, eliminar_item_del_carrito, convertir_carrito_a_pedido
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from django.conf import settings
from .models import Cliente
from functools import wraps
from jose import jwt
import requests

# API View para obtener toda la información
@swagger_auto_schema(method='get', operation_description="Obtener toda la información de productos, tallas, pedidos, etc.")
@keycloak_protected
@api_view(['GET'])
def allInfo(request):
    data = {
        "clientes": ClienteSerializer(Cliente.objects.all(), many=True).data,
        "categorias": CategoriaSerializer(Categoria.objects.all(), many=True).data,
        "marcas": MarcaSerializer(Marca.objects.all(), many=True).data,
        "tallas": TallaSerializer(Talla.objects.all(), many=True).data,
        "colores": ColorSerializer(Color.objects.all(), many=True).data,
        "productos": ProductoSerializer(Producto.objects.all(), many=True).data,
        "producto_imagenes": ProductoImagenSerializer(ProductoImagen.objects.all(), many=True).data,
        "productos_talla_color": ProductoTallaColorSerializer(ProductoTallaColor.objects.all(), many=True).data,
        "carritos": CarritoSerializer(Carrito.objects.all(), many=True).data,
        "carrito_items": ItemCarritoSerializer(ItemCarrito.objects.all(), many=True).data,
        "pedidos": PedidoSerializer(Pedido.objects.all(), many=True).data,
        "detalles_pedido": DetallePedidoSerializer(DetallePedido.objects.all(), many=True).data,
        "pagos": PagoSerializer(Pago.objects.all(), many=True).data
    }
    
    return JsonResponse(data, status=status.HTTP_200_OK)

@method_decorator(keycloak_protected, name='dispatch')
class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    #permission_classes = [IsAuthenticated, KeycloakPermission]
    
    #permission_classes = [IsAuthenticated]

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

# @method_decorator(keycloak_protected, name='dispatch')
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
    
    # @swagger_auto_schema(
    #     operation_description="Filtra productos por categoría",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'categoria', 
    #             openapi.IN_QUERY,
    #             description="ID de la categoría", 
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: ProductoSerializer(many=True)}
    # )
    # @action(detail=False, methods=['get'])
    # def por_categoria(self, request):
    #     categoria_id = request.query_params.get('categoria')
    #     if categoria_id:
    #         productos = self.queryset.filter(categoria_id=categoria_id)
    #     else:
    #         productos = self.queryset.all()
        
    #     serializer = self.get_serializer(productos, many=True)
    #     return Response(serializer.data)
    
    # @swagger_auto_schema(
    #     operation_description="Filtra productos por marca",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'marca', 
    #             openapi.IN_QUERY,
    #             description="ID de la marca", 
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: ProductoSerializer(many=True)}
    # )
    # @action(detail=False, methods=['get'])
    # def por_marca(self, request):
    #     marca_id = request.query_params.get('marca')
    #     if marca_id:
    #         productos = self.queryset.filter(marca_id=marca_id)
    #     else:
    #         productos = self.queryset.all()
        
    #     serializer = self.get_serializer(productos, many=True)
    #     return Response(serializer.data)

class ProductoImagenViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar Imagenes de productos
    """
    queryset = ProductoImagen.objects.all()
    serializer_class = ProductoImagenSerializer     
    
    @swagger_auto_schema(
        operation_description="Lista todas las imagenes de productos",
        responses={200: ProductoImagenSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva imagen de producto",
        request_body=ProductoImagenSerializer,
        responses={201: ProductoImagenSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de una imagen de producto específica",
        responses={200: ProductoImagenSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza una imagen de producto existente",
        request_body=ProductoImagenSerializer,
        responses={200: ProductoImagenSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente una imagen de producto existente",
        request_body=ProductoImagenSerializer,
        responses={200: ProductoImagenSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina una imagen de producto",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# @method_decorator(keycloak_protected, name='dispatch')
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

class CarritoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar carritos
    """
    
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @swagger_auto_schema(
        operation_description="Agrega un producto (variación) al carrito.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["variacion_id", "cantidad"],
            properties={
                "variacion_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "cantidad": openapi.Schema(type=openapi.TYPE_INTEGER)
            },
        ),
        responses={200: ItemCarritoSerializer()}
    )
    @action(detail=True, methods=['post'], url_path='agregar-item')
    def agregar_item(self, request, pk=None):
        carrito = self.get_object()
        variacion_id = request.data.get('variacion_id')
        cantidad = request.data.get('cantidad', 1)

        if not variacion_id:
            return Response({'error': 'variacion_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            variacion = ProductoTallaColor.objects.get(id=variacion_id)
        except ProductoTallaColor.DoesNotExist:
            return Response({'error': 'ProductoTallaColor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, variacion=variacion)
        if not creado:
            item.cantidad += int(cantidad)
        else:
            item.cantidad = int(cantidad)
        item.save()

        return Response(ItemCarritoSerializer(item).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualiza la cantidad de un producto en el carrito.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["item_id", "cantidad"],
            properties={
                "item_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "cantidad": openapi.Schema(type=openapi.TYPE_INTEGER)
            },
        ),
        responses={200: ItemCarritoSerializer()}
    )
    @action(detail=True, methods=['post'], url_path='actualizar-item')
    def actualizar_item(self, request, pk=None):
        carrito = self.get_object()
        item_id = request.data.get('item_id')
        cantidad = request.data.get('cantidad')

        if not item_id or not cantidad:
            return Response({'error': 'item_id y cantidad son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = ItemCarrito.objects.get(id=item_id, carrito=carrito)
        except ItemCarrito.DoesNotExist:
            return Response({'error': 'Item no encontrado en este carrito'}, status=status.HTTP_404_NOT_FOUND)

        item.cantidad = int(cantidad)
        item.save()
        return Response(ItemCarritoSerializer(item).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Elimina un item del carrito.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["item_id"],
            properties={
                "item_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={204: 'Item eliminado correctamente'}
    )
    @action(detail=True, methods=['post'], url_path='eliminar-item')
    def eliminar_item(self, request, pk=None):
        carrito = self.get_object()
        item_id = request.data.get('item_id')

        if not item_id:
            return Response({'error': 'item_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = ItemCarrito.objects.get(id=item_id, carrito=carrito)
        except ItemCarrito.DoesNotExist:
            return Response({'error': 'Item no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({'mensaje': 'Item eliminado'}, status=status.HTTP_204_NO_CONTENT)

class CarritoPagarViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar carritos
    """
    
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=True, methods=['post'], url_path='pagar')
    def pagar_carrito(self, request, pk=None):
        carrito = self.get_object()

        if carrito.items.count() == 0:
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        pedido = Pedido.objects.create(
            usuario=carrito.usuario,
            fecha_pedido=timezone.now(),
            estado="pendiente"
        )

        for item in carrito.items.all():
            DetallePedido.objects.create(
                pedido=pedido,
                variacion=item.variacion,
                cantidad=item.cantidad,
                precio_unitario=item.variacion.precio
            )
            item.variacion.stock -= item.cantidad
            item.variacion.save()

        carrito.delete()  # O puedes marcarlo como inactivo

        return Response({"mensaje": f"Pedido {pedido.id} creado con éxito"}, status=status.HTTP_201_CREATED)

class ItemCarritoViewSet(viewsets.ModelViewSet):
    """
    API endpoints para gestionar items de carrito
    """
    
    queryset = ItemCarrito.objects.all()
    serializer_class = ItemCarritoSerializer

    @swagger_auto_schema(
        operation_description="Listar todos los items de carrito",
        responses={200: ItemCarritoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="Crea un nuevo item de carrito", request_body=ItemCarritoCreateSerializer, responses={201: ItemCarritoSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtiene detalles de un item de carrito específico",
        responses={200: ItemCarritoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza un item de carrito existente",
        request_body=ItemCarritoSerializer,
        responses={200: ItemCarritoSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualiza parcialmente un item de carrito existente",
        request_body=ItemCarritoSerializer,
        responses={200: ItemCarritoSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Elimina un item de carrito",
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
    
@api_view(['GET'])
def imagenes_marcas(request):
    data = [
        {
            "nombre": marca.nombre,
            "imagen_url": request.build_absolute_uri(marca.imagen.url) if marca.imagen else None
        }
        for marca in Marca.objects.all()
    ]
    return Response(data)