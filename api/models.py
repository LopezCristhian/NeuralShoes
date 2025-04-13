import uuid # Importar uuid para generar IDs únicos
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, blank=True)  

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.nombre

class Talla(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.numero

class TallaProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tallas = models.ManyToManyField(Talla, blank=True)  
    stock = models.IntegerField(default=0)

    def __str__(self):
        tallas = ", ".join([talla.numero for talla in self.tallas.all()])
        return f"{self.producto.nombre} - {tallas}" if tallas else self.producto.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    
    def __str__(self):
        return f'{self.cliente.nombre} - {self.estado}'

# En este modelo hay que controlar que se pueda hacer varios pedidos en un mismo de talle
# por ejemplo que se pueda comprar un producto x en diferentes tallas
class DetallePedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    talla_producto = models.ForeignKey(TallaProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        unique_together = ('pedido', 'talla_producto')
    
    
    def clean(self):
        if self.talla_producto.stock < self.cantidad:
            raise ValidationError(f"Stock insuficiente para {self.talla_producto.producto.nombre} con talla(s): {', '.join([t.numero for t in self.talla_producto.tallas.all()])}")

    def save(self, *args, **kwargs):
        self.clean() 

        self.precio_unitario = self.talla_producto.producto.precio

        if not self.pk:
            self.talla_producto.stock -= self.cantidad
            self.talla_producto.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pedido.cliente.nombre} - {self.pedido.estado} - {self.talla_producto.producto.nombre}"

class Pago(models.Model):
    METODOS_PAGO = [
        ('Tarjeta', 'Tarjeta'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('PayPal', 'PayPal'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        detalles = DetallePedido.objects.filter(pedido=self.pedido)
        total = sum([detalle.precio_unitario * detalle.cantidad for detalle in detalles])
        self.monto = total
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.pedido.cliente.nombre} - {self.pedido.estado} - {self.metodo_pago}"