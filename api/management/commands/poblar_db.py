from django.core.management.base import BaseCommand
from api.models import Cliente, Categoria, Marca, Producto, Talla, TallaProducto
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos realistas para una tienda de zapatos'

    def handle(self, *args, **kwargs):
        fake = Faker('es_MX')

        # --- ELIMINAR TODOS LOS DATOS (puedes comentar estas líneas después de limpiar la base) ---
        TallaProducto.objects.all().delete()
        Producto.objects.all().delete()
        Marca.objects.all().delete()
        Categoria.objects.all().delete()
        Talla.objects.all().delete()
        Cliente.objects.all().delete()
        # --- FIN BLOQUE ELIMINAR ---

        # Categorías típicas de zapatos
        categorias_nombres = [
            "Deportivo", "Casual", "Formal", "Botas", "Sandalias", "Infantil"
        ]
        categorias = []
        for nombre in categorias_nombres:
            cat = Categoria.objects.create(
                nombre=nombre,
                descripcion=""  # Sin descripciones
            )
            categorias.append(cat)

        # Marcas conocidas o inventadas
        marcas_nombres = [
            "Nike", "Adidas", "Puma", "Reebok", "Converse", "Vans", "Flexi", "Andrea"
        ]
        marcas = []
        for nombre in marcas_nombres:
            marca = Marca.objects.create(
                nombre=nombre,
                descripcion=""  # Sin descripciones
            )
            marca.categorias.set(random.sample(categorias, k=random.randint(1, 3)))
            marcas.append(marca)

        # Clientes realistas
        for _ in range(10):
            Cliente.objects.create(
                nombre=fake.name(),
                correo=fake.unique.email(),
                telefono=fake.msisdn()[:15],
                direccion=fake.address()
            )

        # Productos de zapatos (modelos reales y populares)
        nombres_zapatos = [
            "Nike Air Max", "Nike Air Force 1", "Nike Cortez", "Nike Blazer", "Nike Dunk Low",
            "Adidas Superstar", "Adidas Stan Smith", "Adidas Campus", "Adidas Samba", "Adidas Gazelle",
            "Puma Suede", "Puma RS-X", "Puma Cali", "Puma Future Rider",
            "Converse Chuck Taylor", "Converse Run Star Hike", "Converse One Star",
            "Vans Old Skool", "Vans Sk8-Hi", "Vans Authentic", "Vans Era",
            "Reebok Classic Leather", "Reebok Club C", "Reebok Nano",
            "Flexi Casual", "Andrea Comfort", "Andrea Running"
        ]
        productos = []
        for nombre in nombres_zapatos:
            prod = Producto.objects.create(
                nombre=nombre,
                descripcion="",  # Sin descripciones
                precio=round(random.uniform(500, 3000), 2),
                stock=random.randint(10, 100),
                marca=random.choice(marcas)
            )
            productos.append(prod)

        # Tallas típicas de zapatos
        tallas = []
        for numero in range(22, 31):  # Tallas del 22 al 30
            talla = Talla.objects.create(numero=str(numero))
            tallas.append(talla)

        # Relacionar productos con tallas y stock
        for producto in productos:
            tp = TallaProducto.objects.create(
                producto=producto,
                stock=random.randint(5, 30)
            )
            tp.tallas.set(random.sample(tallas, k=random.randint(3, 6)))  # Cada producto tiene varias tallas

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada con modelos reales de zapatos y sin descripciones!'))