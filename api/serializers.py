from .models import Cliente, Categoria, Marca, Talla,  Color, Producto, ProductoImagen, ProductoTallaColor, Carrito, ItemCarrito, Pedido, DetallePedido, Pago
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)  # Relación para mostrar categorías
    categorias_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, source='categorias', write_only=True
    )  # Relación para crear la marca y asociar categorías por ID

    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'categorias', 'categorias_id']

    def create(self, validated_data):
        categorias_data = validated_data.pop('categorias', [])  # Obtener categorías
        marca = Marca.objects.create(**validated_data)  # Crear la marca
        marca.categorias.set(categorias_data)  # Asociar las categorías
        return marca
    
class TallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = '__all__'
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = ['id', 'imagen']

class ProductoSerializer(serializers.ModelSerializer):
    imagenes = ProductoImagenSerializer(many=True, read_only=True)  # Relación para las imágenes
    
    marca = MarcaSerializer(read_only=True)  # Mostrar información de la marca
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(), source='marca', write_only=True
    )  # Relación para crear producto y asociar marca por ID
    colores = ColorSerializer(many=True, read_only=True)  # Relación para los colores
    tallas = TallaSerializer(many=True, read_only=True)  # Relación para las tallas

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock_total', 'imagenes', 'marca', 'colores', 'tallas', 'marca_id']
        
    def get_marca(self, obj):
        if obj.marca:
            return {
                'id': str(obj.marca.id),
                'nombre': obj.marca.nombre
            }
        return None

class ProductoTallaColorSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    talla = TallaSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    
    producto_id = serializers.PrimaryKeyRelatedField(
    queryset=Producto.objects.all(), source='producto', write_only=True
    )
    
    tallas_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Talla.objects.all()), source='talla', write_only=True
    )  # Relación para asociar tallas por ID
    
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True
        )
    
    class Meta:
        model = ProductoTallaColor
        fields = ['id', 'producto', 'producto_id', 'talla', 'color', 'tallas_ids', 'color_id', 'stock']
        
    # def create(self, validated_data):
    #     tallas = validated_data.pop('tallas_ids', None)  # Obtener las tallas
    #     color = validated_data.pop('color_id', None)  # Obtener el color
        
    #     producto = Producto.objects.get(id=validated_data.pop('producto_id'))  # Obtener el producto
        
    #     producto_talla_color = ProductoTallaColor.objects.create(producto=producto, talla=tallas[0], color=color, stock=validated_data.get('stock', 0))  # Crear la variación de producto
        
    #     if tallas is not None:
    #         producto_talla_color.tallas.set(tallas)  # Asociar las tallas
            
    #     return producto_talla_color
    
    def update(self, instance, validated_data):
        tallas = validated_data.pop('tallas_ids', None)  # Obtener las tallas
        color = validated_data.pop('color_id', None)  # Obtener el color
        
        instance.producto = validated_data.get('producto', instance.producto)
        instance.talla = validated_data.get('talla', instance.talla)
        instance.color = validated_data.get('color', instance.color)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        
        if tallas is not None:
            instance.tallas.set(tallas)  # Actualizar tallas asociadas
            
        return instance   
    
class ProductoTallaColorCreateSerializer(serializers.Serializer):
    producto_id = serializers.UUIDField()  # ID del producto
    talla_id = serializers.UUIDField()  # ID de la talla
    color_id = serializers.UUIDField()  # ID del color
    stock = serializers.IntegerField()  # Stock de la variación   
    
class ItemCarritoSerializer(serializers.ModelSerializer):
    variacion = ProductoTallaColorSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'variacion', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.cantidad * obj.variacion.precio

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'cliente', 'actualizado', 'items', 'total']

    def get_total(self, obj):
        return sum([item.cantidad * item.variacion.precio for item in obj.items.all()])

class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)  # Mostrar datos del cliente
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source='cliente', write_only=True
    )  # Relación para asociar cliente por ID

    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoCreateSerializer(serializers.Serializer):
    cliente_id = serializers.UUIDField()  # ID del cliente
    estado = serializers.CharField()  # Estado del pedido

class DetallePedidoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    pedido_id = serializers.PrimaryKeyRelatedField(
        queryset=Pedido.objects.all(), source='pedido', write_only=True
    )  # Relación para asociar pedido por ID
    producto_talla_color = ProductoTallaColorSerializer(read_only=True)  # Relación con ProductoTallaColor
    producto_talla_color_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductoTallaColor.objects.all(), source='producto_talla_color', write_only=True
    )  # Relación para asociar ProductoTallaColor por ID

    class Meta:
        model = DetallePedido
        fields = ['id', 'pedido_id', 'producto_talla_color', 'producto_talla_color_id', 'pedido', 'cantidad']

class DetallePedidoCreateSerializer(serializers.Serializer):
    pedido_id = serializers.UUIDField()  # ID del pedido
    producto_talla_color_id = serializers.UUIDField()  # ID de la variación de producto (talla y color)
    cantidad = serializers.IntegerField()  # Cantidad del producto

    def validate(self, data):
        producto_talla_color = ProductoTallaColor.objects.get(id=data['producto_talla_color_id'])  # Obtener la variación del producto
        if producto_talla_color.stock < data['cantidad']:  # Validar si hay suficiente stock
            raise serializers.ValidationError("Stock insuficiente para esta talla y color")
        return data

class PagoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)  # Mostrar los detalles del pedido
    pedido_id = serializers.PrimaryKeyRelatedField(
        queryset=Pedido.objects.all(), source='pedido', write_only=True
    )  # Relación para asociar pedido por ID

    class Meta:
        model = Pago
        fields = ['id', 'pedido_id', 'metodo_pago', 'pedido']

class PagoCreateSerializer(serializers.Serializer):
    pedido_id = serializers.UUIDField()  # ID del pedido
    metodo_pago = serializers.CharField()  # Método de pago