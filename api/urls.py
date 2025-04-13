from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, CategoriaViewSet,MarcaViewSet, ProductoViewSet, 
    TallaViewSet, TallaProductoViewSet, PedidoViewSet, 
    DetallePedidoViewSet, PagoViewSet
)

from .views import obtener_toda_la_info

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'tallas', TallaViewSet)
router.register(r'talla-productos', TallaProductoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('toda-la-info/', obtener_toda_la_info, name='toda-la-info'),
]