from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import allInfo

from .views import (
    ClienteViewSet, 
    CategoriaViewSet,
    MarcaViewSet,
    TallaViewSet,
    ColorViewSet,
    ProductoViewSet, 
    ProductoImagenViewSet,
    ProductoTallaColorViewSet,
    CarritoViewSet,
    ItemCarritoViewSet,
    PedidoViewSet,
    DetallePedidoViewSet,
    PagoViewSet
)


router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'tallas', TallaViewSet)
router.register(r'colores', ColorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'producto-imagenes', ProductoImagenViewSet)
router.register(r'productos-talla-color', ProductoTallaColorViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'carrito-items', ItemCarritoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all/', allInfo, name='allInfo' ),
]