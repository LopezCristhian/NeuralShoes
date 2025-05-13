from django.contrib import admin
from api.models import Cliente, Categoria, Producto, Talla, TallaProducto, Pedido, DetallePedido, Pago, Marca

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono', 'direccion', 'fecha_registro')
    search_fields = ('id', 'nombre', 'correo', 'telefono', 'direccion')
    date_hierarchy = 'fecha_registro'
    
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion',  )
    search_fields = ('id', 'nombre', 'descripcion')
    
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'imagen', 'mostrar_categorias')
    search_fields = ('id', 'nombre', 'descripcion', 'mostrar_categorias')
    list_filter = ('categorias',)
    filter_horizontal = ('categorias',)
    
    def mostrar_categorias(self, obj):
        return ", ".join([categoria.nombre for categoria in obj.categorias.all()])
    
    mostrar_categorias.short_description = 'Categorías'  

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'stock_total', 'imagen', 'marca')
    search_fields = ('id', 'nombre', 'descripcion', 'precio', 'stock_total', 'marca')
    list_filter = ('marca',)
    
    readonly_fields = ('stock_total',)

class TallaAdmin(admin.ModelAdmin): 
    list_display = ('id', 'numero',)
    search_fields = ('id', 'numero',)

class TallaProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'mostrar_tallas', 'stock_talla')
    search_fields = ('id', 'producto', 'mostrar_tallas', 'stock_talla')
    
    filter_horizontal = ('tallas',)
    
    def mostrar_tallas(self, obj):
        return ", ".join([talla.numero for talla in obj.tallas.all()])

    mostrar_tallas.short_description = 'Tallas'  

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado')
    search_fields = ('id', 'cliente', 'fecha_pedido', 'estado')
    list_filter = ('id', 'cliente', 'fecha_pedido', 'estado')
    date_hierarchy = 'fecha_pedido'
    
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'mostrar_talla_producto', 'cantidad', 'precio_unitario')
    search_fields = ('id', 'pedido', 'cantidad', 'precio_unitario')
    list_filter = ('id', 'pedido', 'cantidad', 'precio_unitario')
    #filter_horizontal = ('mostrar_talla_producto',)
    readonly_fields = ('precio_unitario',)
    #exclude = ('precio_unitario',)
    
    def mostrar_talla_producto(self, obj):
        tallas = ", ".join([tallas.numero for tallas in obj.talla_producto.tallas.all()])
        return f"{obj.talla_producto.producto.nombre} - {tallas}" if tallas else obj.talla_producto.producto.nombre 
    
    mostrar_talla_producto.short_description = 'Producto - Talla'

class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'metodo_pago', 'monto', 'fecha_pago')
    search_fields = ('id','pedido', 'metodo_pago', 'monto', 'fecha_pago')
    list_filter = ('id','pedido', 'metodo_pago', 'monto', 'fecha_pago')
    date_hierarchy = 'fecha_pago'
    readonly_fields = ('monto',)
    #exclude = ('monto',)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Talla, TallaAdmin)
admin.site.register(TallaProducto, TallaProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Marca, MarcaAdmin)