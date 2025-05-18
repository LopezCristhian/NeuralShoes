from api.models import Cliente, Categoria, Marca, Talla, Color, Producto, ProductoTallaColor, Pedido, DetallePedido, Pago
from django.contrib import admin

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono', 'direccion', 'fecha_registro')
    search_fields = ('id', 'nombre', 'correo', 'telefono', 'direccion')
    date_hierarchy = 'fecha_registro'
    
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion',)
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
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'stock_total', 'imagen',  'mostrar_colores', 'mostrar_tallas')
    search_fields = ('id', 'nombre', 'descripcion', 'precio', 'stock_total', 'marca')
    list_filter = ('marca', 'colores', 'tallas')
    #filter_horizontal = ('colores', 'tallas')
    
    readonly_fields = ('stock_total',)
    
    def mostrar_colores(self, obj):
        return ", ".join([color.nombre for color in obj.colores.all()])
    mostrar_colores.short_description = 'Colores'
    
    def mostrar_tallas(self, obj):
        return ", ".join([talla.numero for talla in obj.tallas.all()])
    mostrar_tallas.short_description = 'Tallas'

class TallaAdmin(admin.ModelAdmin): 
    list_display = ('id', 'numero',)
    search_fields = ('id', 'numero',)
    list_filter = ('id', 'numero',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    search_fields = ('id', 'nombre',)
    list_filter = ('id', 'nombre',)

class ProductoTallaColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'talla', 'color', 'stock')
    search_fields = ('id', 'producto', 'mostrar_tallas', 'mostrar_colores', 'stock')
    
    list_filter = ('producto', 'talla', 'color')
    
    def mostrar_tallas(self, obj):
        return ", ".join([talla.numero for talla in obj.talla.all()])
    
    mostrar_tallas.short_description = 'Tallas'
    
    def mostrar_colores(self, obj):
        return ", ".join([color.nombre for color in obj.color.all()])
    
    mostrar_colores.short_description = 'Colores'

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado')
    search_fields = ('id', 'cliente', 'fecha_pedido', 'estado')
    list_filter = ('id', 'cliente', 'fecha_pedido', 'estado')
    date_hierarchy = 'fecha_pedido'
    
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'mostrar_producto_talla_color', 'cantidad', 'precio_unitario')
    search_fields = ('id', 'pedido', 'cantidad', 'precio_unitario')
    list_filter = ('id', 'pedido', 'cantidad', 'precio_unitario')
    
    readonly_fields = ('precio_unitario',)
    
    def mostrar_producto_talla_color(self, obj):
        return f"{obj.variacion.producto.nombre} - Talla: {obj.variacion.talla.numero} - Color: {obj.variacion.color.nombre}"
    
    mostrar_producto_talla_color.short_description = 'Producto - Talla - Color'

class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'metodo_pago', 'monto', 'fecha_pago')
    search_fields = ('id','pedido', 'metodo_pago', 'monto', 'fecha_pago')
    list_filter = ('id','pedido', 'metodo_pago', 'monto', 'fecha_pago')
    date_hierarchy = 'fecha_pago'
    readonly_fields = ('monto',)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Talla, TallaAdmin)
admin.site.register(Color, ColorAdmin)  # Registro de Color
admin.site.register(ProductoTallaColor, ProductoTallaColorAdmin)  # Registro de ProductoTallaColor
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Pago, PagoAdmin)