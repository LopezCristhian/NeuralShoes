from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
from django.db import transaction
from django.db import models
import uuid # Importar uuid para generar IDs únicos

# Create your models here.

class Cliente(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    imagen = models.ImageField(upload_to='brands', blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, blank=True)  

    def __str__(self):
        return self.nombre

class Talla(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.numero

class Color(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_total = models.IntegerField(default=0, blank=True, null=True)
    #imagen = models.ImageField(upload_to='products', blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    colores = models.ManyToManyField(Color, through='ProductoTallaColor')
    tallas = models.ManyToManyField(Talla, through='ProductoTallaColor')

    def __str__(self):
        return self.nombre

class ProductoImagen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='products/')
    #descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class ProductoTallaColor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'talla', 'color')  # Evitar duplicados

    def __str__(self):
        return f"{self.producto.nombre} - Talla: {self.talla.numero} - Color: {self.color.nombre}"

    def restar_stock(self, cantidad):
        """Restar el stock de esta combinación de producto, talla y color."""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            self.producto.stock_total -= cantidad
        else:
            raise ValidationError(f"Stock insuficiente para {self.producto.nombre} - Talla: {self.talla.numero} - Color: {self.color.nombre}")
        
    # Función que actualiza el stock total del producto con stock del producto_talla_color
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.producto.stock_total = sum([variacion.stock for variacion in ProductoTallaColor.objects.filter(producto=self.producto)])
        self.producto.save()        
        
class Carrito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='carritos')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def total(self):
        return sum([item.subtotal() for item in self.items.all()])

    def __str__(self):
        return f"Carrito de {self.cliente.nombre} ({self.id})"

class ItemCarrito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    variacion = models.ForeignKey('ProductoTallaColor', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'variacion')  # evita duplicados

    def subtotal(self):
        return self.variacion.producto.precio * self.cantidad
    
    # Qur no supere el stock total del producto
    def clean(self):
        if self.cantidad > self.variacion.producto.stock_total:
            raise ValidationError(f"Cantidad excede el stock total del producto {self.variacion.producto.nombre}")     

    def __str__(self):
        return f"{self.variacion} x {self.cantidad}"

def agregar_o_actualizar_item(carrito, variacion, cantidad):
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, variacion=variacion)
    
    if cantidad <= 0:
        item.delete()
    else:
        if cantidad > variacion.stock:
            raise ValidationError(f"Stock insuficiente para {variacion}")
        item.cantidad = cantidad
        item.save()

def convertir_carrito_a_pedido(carrito):
    if not carrito.items.exists():
        raise ValidationError("El carrito está vacío.")

    with transaction.atomic():
        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente=carrito.cliente,
            estado='Pendiente'
        )

        for item in carrito.items.all():
            variacion = item.variacion
            cantidad = item.cantidad

            if variacion.stock < cantidad:
                raise ValidationError(f"Stock insuficiente para {variacion}")

            # Crear detalle de pedido (esto ya descuenta stock automáticamente)
            DetallePedido.objects.create(
                pedido=pedido,
                variacion=variacion,
                cantidad=cantidad
            )

        # Marcar el carrito como inactivo o eliminarlo
        carrito.activo = False
        carrito.save()

        return pedido

def eliminar_item_del_carrito(carrito, variacion):
    ItemCarrito.objects.filter(carrito=carrito, variacion=variacion).delete()

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

class DetallePedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    variacion = models.ForeignKey(ProductoTallaColor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.variacion.stock < self.cantidad:
            raise ValidationError(f"Stock insuficiente para {self.variacion.producto.nombre} - Talla: {self.variacion.talla.numero} - Color: {self.variacion.color.nombre}")

    def save(self, *args, **kwargs):
        self.clean()
        self.precio_unitario = self.variacion.producto.precio

        # Descontar stock
        self.variacion.restar_stock(self.cantidad)

        # Actualizar stock total del producto
        self.variacion.producto.stock_total -= self.cantidad

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pedido.cliente.nombre} - {self.variacion}"

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