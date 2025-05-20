from django.core.management.base import BaseCommand
from api.models import Cliente, Categoria, Marca, Producto, Talla, Color, ProductoTallaColor
from faker import Faker
import random
import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos realistas y descarga imágenes webp para las marcas'

    def handle(self, *args, **kwargs):
        fake = Faker('es_MX')

        # --- ELIMINAR TODOS LOS DATOS ---
        ProductoTallaColor.objects.all().delete()
        Producto.objects.all().delete()
        Marca.objects.all().delete()
        Categoria.objects.all().delete()
        Talla.objects.all().delete()
        Color.objects.all().delete()
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

        # Marcas y productos reales asociados
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

        # URLs de imágenes webp de marcas (puedes cambiarlas por otras si lo deseas)
        marcas_imagenes = {
            "Nike": "https://logo.clearbit.com/nike.com",
            "Adidas": "https://logo.clearbit.com/adidas.com",
            "Puma": "https://logo.clearbit.com/puma.com",
            "Reebok": "https://logo.clearbit.com/reebok.com",
            "Jordan": "https://logo.clearbit.com/jordan.com",
            "New Balance": "https://logo.clearbit.com/newbalance.com",
            "Converse": "https://logo.clearbit.com/converse.com",
            "Vans": "https://logo.clearbit.com/vans.com",
            "Skechers": "https://logo.clearbit.com/skechers.com"
        }

        # Marcas
        marcas = {}
        for marca_nombre in marcas_productos.keys():
            cats = [c for c in categorias if c.nombre in ["Deportivo", "Casual", "Infantil"]]
            marca = Marca(nombre=marca_nombre, descripcion="")
            marca.save()
            marca.categorias.set(cats)
            # Descargar imagen y asignar
            url = marcas_imagenes.get(marca_nombre)
            if url:
                try:
                    img_temp = NamedTemporaryFile(delete=True, suffix=".png")
                    response = requests.get(url)
                    img_temp.write(response.content)
                    img_temp.flush()
                    marca.imagen.save(f"{marca_nombre}.png", File(img_temp), save=True)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"No se pudo descargar la imagen de {marca_nombre}: {e}"))
            marcas[marca_nombre] = marca

        # Clientes
        for _ in range(10):
            Cliente.objects.create(
                nombre=fake.name(),
                correo=fake.unique.email(),
                telefono=fake.msisdn()[:15],
                direccion=fake.address()
            )

        # Colores básicos
        colores_nombres = ["Negro", "Blanco", "Rojo", "Azul", "Gris", "Verde", "Amarillo"]
        colores = []
        for nombre in colores_nombres:
            color = Color.objects.create(nombre=nombre)
            colores.append(color)

        # Productos
        productos = []
        for marca_nombre, modelos in marcas_productos.items():
            for modelo in modelos:
                prod = Producto.objects.create(
                    nombre=modelo,
                    descripcion="",
                    precio=round(random.uniform(800, 3000), 2),
                    marca=marcas[marca_nombre]
                )
                productos.append(prod)

        # Tallas
        tallas = []
        for numero in range(22, 31):  # Tallas del 22 al 30
            talla = Talla.objects.create(numero=str(numero))
            tallas.append(talla)

        # ProductoTallaColor (relaciona productos con tallas y colores)
        for producto in productos:
            tallas_producto = random.sample(tallas, k=random.randint(3, 6))
            colores_producto = random.sample(colores, k=random.randint(2, 4))
            for talla in tallas_producto:
                for color in colores_producto:
                    ProductoTallaColor.objects.create(
                        producto=producto,
                        talla=talla,
                        color=color,
                        stock=random.randint(5, 30)
                    )

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada con imágenes webp de marcas!'))