from rest_framework import serializers
from .models import Cliente, Categoria, Marca, Producto, Talla, TallaProducto, Pedido, DetallePedido, Pago

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)  
    categorias_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, source='categorias', write_only=True
    )  

    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion', 'categorias', 'categorias_id']

    def create(self, validated_data):
        categorias_data = validated_data.pop('categorias', [])  
        marca = Marca.objects.create(**validated_data)  
        marca.categorias.set(categorias_data)  
        return marca

class ProductoSerializer(serializers.ModelSerializer):
    marca = serializers.SerializerMethodField(read_only=True)

    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(),
        source='marca',
        write_only=True
    )

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'marca', 'marca_id']

    def get_marca(self, obj):
        if obj.marca:
            return {
                'id': str(obj.marca.id),
                'nombre': obj.marca.nombre
            }
        return None

class TallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = '__all__'

class TallaProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )
    tallas = TallaSerializer(many=True, read_only=True)
    tallas_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Talla.objects.all()),
        source='tallas',
        write_only=True
    )

    class Meta:
        model = TallaProducto
        fields = ['id', 'producto', 'producto_id', 'tallas', 'tallas_ids', 'stock']

    def update(self, instance, validated_data):
        tallas = validated_data.pop('tallas', None)

  
        instance.stock = validated_data.get('stock', instance.stock)
        instance.producto = validated_data.get('producto', instance.producto)
        instance.save()


        if tallas is not None:
            instance.tallas.set(tallas)

        return instance

class TallaProductoCreateSerializer(serializers.Serializer):
    producto_id = serializers.UUIDField()
    tallas_ids = serializers.ListField(child=serializers.UUIDField())
    stock = serializers.IntegerField()

class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source='cliente', write_only=True
    )

    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoCreateSerializer(serializers.Serializer):
    cliente_id = serializers.UUIDField()
    estado = serializers.CharField()

class DetallePedidoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    pedido_id = serializers.PrimaryKeyRelatedField(
        queryset=Pedido.objects.all(), source='pedido', write_only=True
    )
    talla_producto = TallaProductoSerializer(read_only=True)
    talla_producto_id = serializers.PrimaryKeyRelatedField(
        queryset=TallaProducto.objects.all(), source='talla_producto', write_only=True
    )

    class Meta:
        model = DetallePedido
        fields = 'id', 'pedido_id', 'talla_producto', 'talla_producto_id', 'pedido', 'cantidad',

class DetallePedidoCreateSerializer(serializers.Serializer):
    pedido_id = serializers.UUIDField()
    talla_producto_id = serializers.UUIDField()
    cantidad = serializers.IntegerField()   
    
class PagoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    pedido_id = serializers.PrimaryKeyRelatedField(
        queryset=Pedido.objects.all(), source='pedido', write_only=True
    )

    class Meta:
        model = Pago
        fields = 'id', 'pedido_id', 'metodo_pago', 'pedido'
        
class PagoCreateSerializer(serializers.Serializer):
    pedido_id = serializers.UUIDField()
    metodo_pago = serializers.CharField()