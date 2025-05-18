from django.core.management.base import BaseCommand
from api.models import Cliente, Categoria, Marca, Producto, Talla, TallaProducto
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos realistas para una tienda de zapatos (sin pedidos ni pagos)'

    def handle(self, *args, **kwargs):
        fake = Faker('es_MX')

        # --- ELIMINAR TODOS LOS DATOS ---
        TallaProducto.objects.all().delete()
        Producto.objects.all().delete()
        Marca.objects.all().delete()
        Categoria.objects.all().delete()
        Talla.objects.all().delete()
        Cliente.objects.all().delete()
        # --- FIN BLOQUE ELIMINAR ---

        # Categorías
        categorias_nombres = [
            "Deportivo", "Casual", "Formal", "Botas", "Sandalias", "Infantil"
        ]
        categorias = []
        for nombre in categorias_nombres:
            cat = Categoria.objects.create(nombre=nombre, descripcion="")
            categorias.append(cat)

        # Marcas y productos reales asociados (solo las que pediste)
        marcas_productos = {
            "Nike": [
                "Nike Air Max", "Nike Air Force 1", "Nike Cortez", "Nike Blazer", "Nike Dunk Low"
            ],
            "Adidas": [
                "Adidas Superstar", "Adidas Stan Smith", "Adidas Campus", "Adidas Samba", "Adidas Gazelle"
            ],
            "Puma": [
                "Puma Suede", "Puma RS-X", "Puma Cali", "Puma Future Rider"
            ],
            "Reebok": [
                "Reebok Classic Leather", "Reebok Club C", "Reebok Nano"
            ],
            "Jordan": [
                "Air Jordan 1", "Air Jordan 4", "Air Jordan 11", "Jordan Delta", "Jordan Max Aura"
            ],
            "New Balance": [
                "New Balance 574", "New Balance 327", "New Balance 990", "New Balance 1080"
            ],
            "Converse": [
                "Converse Chuck Taylor", "Converse Run Star Hike", "Converse One Star"
            ],
            "Vans": [
                "Vans Old Skool", "Vans Sk8-Hi", "Vans Authentic", "Vans Era"
            ],
            "Skechers": [
                "Skechers D'Lites", "Skechers Go Walk", "Skechers Flex Advantage"
            ]
        }

        # Marcas
        marcas = {}
        for marca_nombre in marcas_productos.keys():
            cats = [c for c in categorias if c.nombre in ["Deportivo", "Casual", "Infantil"]]
            marca = Marca.objects.create(nombre=marca_nombre, descripcion="")
            marca.categorias.set(cats)
            marcas[marca_nombre] = marca

        # Clientes
        for _ in range(10):
            Cliente.objects.create(
                nombre=fake.name(),
                correo=fake.unique.email(),
                telefono=fake.msisdn()[:15],
                direccion=fake.address()
            )

        # Productos
        productos = []
        for marca_nombre, modelos in marcas_productos.items():
            for modelo in modelos:
                prod = Producto.objects.create(
                    nombre=modelo,
                    descripcion="",
                    precio=round(random.uniform(800, 3000), 2),
                    stock=random.randint(10, 100),
                    marca=marcas[marca_nombre]
                )
                productos.append(prod)

        # Tallas
        tallas = []
        for numero in range(22, 31):  # Tallas del 22 al 30
            talla = Talla.objects.create(numero=str(numero))
            tallas.append(talla)

        # TallaProducto (relaciona productos con tallas)
        for producto in productos:
            tp = TallaProducto.objects.create(
                producto=producto,
                stock=random.randint(5, 30)
            )
            tp.tallas.set(random.sample(tallas, k=random.randint(3, 6)))

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada mi lidel!'))