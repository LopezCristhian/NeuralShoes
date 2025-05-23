# Generated by Django 5.2 on 2025-05-07 02:25

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='brands')),
                ('categorias', models.ManyToManyField(blank=True, to='api.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado'), ('Cancelado', 'Cancelado')], max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('metodo_pago', models.CharField(choices=[('Tarjeta', 'Tarjeta'), ('Efectivo', 'Efectivo'), ('Transferencia', 'Transferencia'), ('PayPal', 'PayPal')], max_length=50)),
                ('monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_total', models.IntegerField(blank=True, default=0, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='products')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.marca')),
            ],
        ),
        migrations.CreateModel(
            name='TallaProducto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('stock_talla', models.IntegerField(default=0)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producto')),
                ('tallas', models.ManyToManyField(blank=True, to='api.talla')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pedido')),
                ('talla_producto', models.ManyToManyField(blank=True, to='api.tallaproducto')),
            ],
        ),
    ]
