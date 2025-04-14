# NeuralShoes
Tienda de calzado (Proyecto modelos de computación)

# Descripción del proyecto NeuralShoes - Sistema de Gestión de Ventas de Calzado

## Descripción del Proyecto
NeuralShoes es un sistema de gestión de ventas de calzado desarrollado con Django y Django REST Framework. Su objetivo es permitir la administración eficiente de clientes, productos, pedidos y pagos, brindando una solución robusta para tiendas de calzado.

## Características Principales
- **Gestión de Clientes**: Registro, actualización y consulta de clientes.
- **Administración de Productos**: Manejo de categorías, marcas, productos y tallas.
- **Control de Inventario**: Asociación de productos con sus respectivas tallas y stock.
- **Gestión de Pedidos**: Creación de pedidos con múltiples productos y diferentes tallas.
- **Procesamiento de Pagos**: Registro de pagos con distintos métodos de pago.
- **API RESTful**: Exposición de endpoints para interactuar con los datos del sistema.

## Tecnologías Utilizadas
- **Backend**: Django, Django REST Framework
- **Base de Datos**: PostgreSQL
- **Contenerización**: Docker
- **Documentación API**: Swagger / OpenAPI

# Intrucciones de despliegue

## Instalación y Configuración
### Requisitos Previos
- Python 3.8+
- PostgreSQL
- Virtualenv (opcional)

### Pasos para la instalación
1. Clonar el repositorio:
   ```sh
   git clone https://github.com/LopezCristhian/NeuralShoes.git
   cd NeuralShoes
   ```
2. Crear y activar un entorno virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Configurar la base de datos en `settings.py`:
   ```python
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': os.environ.get('DB_NAME', 'neuralshoes'),
         'USER': os.environ.get('DB_USER', 'postgres'),
         'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
         'HOST': os.environ.get('DB_HOST', 'localhost'),
         'PORT': os.environ.get('DB_PORT', '5432'),
      }
   }     
   ```
   ## Se resalta que para efectos de desarrollo se se ha usado Sqlite3
5. Aplicar migraciones:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Crear un superusuario:
   ```sh
   python manage.py createsuperuser
   ```
7. Ejecutar el servidor:
   ```sh
   python manage.py runserver
   ```

## Endpoints de la API
La API está documentada en Swagger. Para acceder a la documentación interactiva, ejecutar el servidor y visitar:
```
http://127.0.0.1:8001/swagger/
```

## Contribución
Si deseas contribuir, por favor sigue estos pasos:
1. Haz un fork del repositorio
2. Crea una rama (`git checkout -b feature-nueva`)
3. Realiza tus cambios y commitea (`git commit -m 'Añadir nueva característica'`)
4. Sube los cambios (`git push origin feature-nueva`)
5. Abre un Pull Request

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Docker

- **Dockerfile**:
1. Usa una imagen base de Python:
   ```sh
   FROM python:3.12-slim
   ```
2. Establece el directorio del trabajo:
   ```sh FROM python:3.12-slim ``` Dentro del contenedor, todo se ejecutara en /app

3. Copia dependencias e instálalas
   ```sh 
   COPY backend/requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt
   ```

4. Expone el puerto 8001

5. Ejecuta el servidor de Django
   ```sh
   CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
   ```

- **docker-compose.yml**:
1. Versión del Compose
   ```sh
   version: '3.9'
   ```
2. Servicio de base de datos (PostgreSQL)
Usa la imagen postgres:latest.
Guarda los datos en un volumen postgres_data.
Configura el usuario, contraseña y base de datos.
Expone el puerto 5432.

3. Servicio del backend (Django)
Usa el *Dockerfile* para construir la imagen.
Depende de la base de datos
Expone el puerto 8001 en el host (Django corre en 8001 dentro del contenedor).

4. Volúmenes
postgres_data → Guarda datos persistentes de PostgreSQL.

# Capturas de los Endpoints

## Diagrama E-R DB NeuralShoes
![/assets/diagramaER.png](/assets/diagramaER.png)

## Toda la información de la API

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/toda-la-info/                    Lista toda la información de la API
Devuelve en formato JSON toda la información de la API.
![/assets/image-69.png](/assets/image-69.png)

## Clientes

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/clientes/                    Lista todos los clientes
Devuelve en formato JSON todos los clientes registrados en la base de datos.
![/assets/image-1.png](/assets/image-1.png)

POST                                    http://127.0.0.1:8001/api/clientes/                    Crea un nuevo cliente
Para agregar un nuevo cliente no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image.png](/assets/image.png)

Al volver a hacer el GET se obtiene el cliente creado junto con los anteriormente exitentes.
![/assets/image-2.png](/assets/image-2.png)

GET                                     http://127.0.0.1:8001/api/clientes/{id}/               Obtiene un cliente por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-3.png](/assets/image-3.png)

PUT                                     http://127.0.0.1:8001/api/clientes/{id}/               Actualiza un cliente por su ID
En este caso con el PUT se modifica la dirección del usuario con id = 3 de Pasto a Bogotá.
![/assets/image-4.png](/assets/image-4.png)

Posteriormente se visualiza la nueva dirección del usuario con id = 3.
![/assets/image-5.png](/assets/image-5.png)

DELETE                                  http://127.0.0.1:8001/api/clientes/{id}/               Elimina un cliente por su ID
Elimina al cliente con con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-6.png](/assets/image-6.png)

Se observa los resultados haciendo el GET con el id que tenia el usuario.
![/assets/image-7.png](/assets/image-7.png)

## Categorías
Método   
                               Endpoint                                                     Descripción 
GET                                     http://127.0.0.1:8001/api/categorias/                    Lista todas las categorías
Devuelve en formato JSON todas las categorías registradas en la base de datos.
![/assets/image-8.png](/assets/image-8.png)

POST                                    http://127.0.0.1:8001/api/categorias/                    Crea una nueva categoría
Para agregar una nueva categoría no se especifica el id dado que en los modelos implementados se dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-9.png](/assets/image-9.png)

Al volver a hacer el GET se obtiene la categoría creada junto con las anteriormente exitentes.
![/assets/image-10.png](/assets/image-10.png)

GET                                     http://127.0.0.1:8001/api/categorias/{id}/             Obtiene una categoría por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-11.png](/assets/image-11.png)

PUT                                     http://127.0.0.1:8001/api/categorias/{id}/           Actualiza una categoría por su ID
En este caso se módificará la el nombre de la categoria anteriormente creada.
![/assets/image-12.png](/assets/image-12.png)

Posteriormente se hace la consulta de la categoria con su respectivo id.
![/assets/image-13.png](/assets/image-13.png)

DELETE                                  http://127.0.0.1:8001/api/categorias/{id}/            Elimina una categoría por su ID
Elimina la categoría con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-14.png](/assets/image-14.png)

Se observa los resultados haciendo el GET con el id que tenia el la categoría.
![/assets/image-15.png](/assets/image-15.png)

## Marcas
Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/marcas/                    Lista todas las marcas
Devuelve en formato JSON todas las marcas registradas en la base de datos.
![/assets/image-16.png](/assets/image-16.png)

POST                                    http://127.0.0.1:8001/api/marcas/                    Crea una nueva marca
Para agregar una nueva marca no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-19.png](/assets/image-19.png)

Al volver a hacer el GET se obtiene la marca creada junto con las anteriormente exitentes.
![/assets/image-18.png](/assets/image-18.png)

GET                                     http://127.0.0.1:8001/api/marcas/{id}/               Obtiene una marca por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-20.png](/assets/image-20.png)

PUT                                     http://127.0.0.1:8001/api/marcas/{id}/               Actualiza una marca por su ID
Se modifica la descripción de la marca con el id proporcionado en este caso se modifica la descripción de la marca con id = 3.
![/assets/image-21.png](/assets/image-21.png)

Al volver a hacer el GET con el id correspondiente se obtiene la marca actualizada junto con las anteriormente exitentes.
![/assets/image-22.png](/assets/image-22.png)

DELETE                                  http://127.0.0.1:8001/api/marcas/{id}/               Elimina una marca por su ID
Elimina la marca con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-23.png](/assets/image-23.png)

Se observa los resultados haciendo el GET con el id que tenia la marca.
![/assets/image-24.png](/assets/image-24.png)

## Productos

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/productos/                    Lista todos los productos
Devuelve en formato JSON todos los productos registrados en la base de datos.
![/assets/image-25.png](/assets/image-25.png)

POST                                    http://127.0.0.1:8001/api/productos/                    Crea un nuevo producto
Para agregar un nuevo producto no se especifica el id dado que en los modelos implementados se dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-26.png](/assets/image-26.png)

Al volver a hacer el GET se obtiene el producto creado junto con los anteriormente exitentes.
![/assets/image-27.png](/assets/image-27.png)

GET                                     http://127.0.0.1:8001/api/productos/{id}/               Obtiene un producto por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-28.png](/assets/image-28.png)

PUT                                     http://127.0.0.1:8001/api/productos/{id}/              Actualiza un producto por su ID
Se modifica el precio del producto con el id proporcionado en este caso se modifica el nombre del producto con id = 2.
![/assets/image-29.png](/assets/image-29.png)

Al volver a hacer el GET con el id correspondiente se obtiene el producto actualizado junto con los anteriormente exitentes.
![/assets/image-30.png](/assets/image-30.png)

DELETE                                  http://127.0.0.1:8001/api/productos/{id}/                Elimina un producto por su ID
Elimina el producto con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-31.png](/assets/image-31.png)

## Tallas

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/tallas/                    Lista todas las tallas
Devuelve en formato JSON todas las tallas registradas en la base de datos.
![/assets/image-32.png](/assets/image-32.png)

POST                                    http://127.0.0.1:8001/api/tallas/                    Crea una nueva talla
Para agregar una nueva talla no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-33.png](/assets/image-33.png)

Al volver a hacer el GET se obtiene la talla creada junto con los anteriormente exitentes.
![/assets/image-34.png](/assets/image-34.png)

GET                                     http://127.0.0.1:8001/api/tallas/{id}/               Obtiene una talla por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-35.png](/assets/image-35.png)

PUT                                     http://127.0.0.1:8001/api/tallas/{id}/               Actualiza una talla por su ID
Se modifica el numero de la talla con el id proporcionado en este caso se modifica el numero de la talla con id = 5.
![/assets/image-36.png](/assets/image-36.png)

Al volver a hacer el GET con el id correspondiente se obtiene la talla actualizada junto con los anteriormente exitentes.
![/assets/image-37.png](/assets/image-37.png)

DELETE                                  http://127.0.0.1:8001/api/tallas/{id}/               Elimina una talla por su ID
Elimina la talla con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-38.png](/assets/image-38.png)

## Tallas de Productos

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/tallas-productos/                    Lista todas las tallas de productos
Devuelve en formato JSON todas las tallas de productos registradas en la base de datos.
![/assets/image-39.png](/assets/image-39.png)

POST                                    http://127.0.0.1:8001/api/tallas-productos/           Crea una nueva talla de producto
Para agregar una nueva talla de producto no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-40.png](/assets/image-40.png)

Al volver a hacer el GET se obtiene la talla de producto creada junto con los anteriormente exitentes.
![/assets/image-41.png](/assets/image-41.png)

GET                                     http://127.0.0.1:8001/api/tallas-productos/{id}/               Obtiene una talla de producto por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-42.png](/assets/image-42.png)

PUT                                     http://127.0.0.1:8001/api/tallas-productos/{id}/     Actualiza una talla de producto por su ID
Se modifica la talla de producto con el id proporcionado en este caso se modifica el producto con id = 1.
![/assets/image-43.png](/assets/image-43.png)

Al volver a hacer el GET con el id correspondiente se obtiene la talla de producto actualizada.
![/assets/image-44.png](/assets/image-44.png)

DELETE                                  http://127.0.0.1:8001/api/tallas-productos/{id}/               Elimina una talla de producto por su ID
Elimina la talla de producto con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-45.png](/assets/image-45.png)


## Pedidos

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/pedidos/                    Lista todos los pedidos
Devuelve en formato JSON todos los pedidos registrados en la base de datos.
![/assets/image-46.png](/assets/image-46.png)

POST                                    http://127.0.0.1:8001/api/pedidos/                    Crea un nuevo pedido
Para agregar un nuevo pedido no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-48.png](/assets/image-48.png)

Al volver a hacer el GET se obtiene el pedido creado junto con los anteriormente exitentes.
![/assets/image-49.png](/assets/image-49.png)

GET                                     http://127.0.0.1:8001/api/pedidos/{id}/               Obtiene un pedido por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-50.png](/assets/image-50.png)

PUT                                     http://127.0.0.1:8001/api/pedidos/{id}/               Actualiza un pedido por su ID
Se modifica el estado del pedido con el id proporcionado en este caso se modifica el estado del pedido con id = 1.
![/assets/image-51.png](/assets/image-51.png)

Al volver a hacer el GET con el id correspondiente se obtiene el pedido actualizado en su estado.
![/assets/image-52.png](/assets/image-52.png)

DELETE                                  http://127.0.0.1:8001/api/pedidos/{id}/               Elimina un pedido por su ID
Elimina el pedido con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-53.png](/assets/image-53.png)

## Detalles de Pedidos

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/detalle-pedidos/                    Lista todos los detalles de pedidos
Devuelve en formato JSON todos los detalles de pedidos registrados en la base de datos.
![/assets/image-54.png](/assets/image-54.png)

POST                                    http://127.0.0.1:8001/api/detalle-pedidos/                    Crea un nuevo detalle de pedido
Para agregar un nuevo detalle de pedido no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-55.png](/assets/image-55.png)

Al volver a hacer el GET se obtiene el detalle de pedido creado junto con los anteriormente exitentes.
![/assets/image-56.png](/assets/image-56.png)

GET                                     http://127.0.0.1:8001/api/detalle-pedidos/{id}/               Obtiene un detalle de pedido por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-58.png](/assets/image-58.png)

PUT                                     http://127.0.0.1:8001/api/detalle-pedidos/{id}/               Actualiza un detalle de pedido por su ID
Se modifica la cantidad del detalle de pedido con el id proporcionado en este caso el pedido con id = 2.
![/assets/image-59.png](/assets/image-59.png)

Al volver a hacer el GET con el id correspondiente se obtiene el detalle de pedido actualizado.
![/assets/image-60.png](/assets/image-60.png)

DELETE                                  http://127.0.0.1:8001/api/detalle-pedidos/{id}/               Elimina un detalle de pedido por su ID
Elimina el detalle de pedido con el id proporcionado en este caso el que se ha usado de ejemplo.
![/assets/image-61.png](/assets/image-61.png)

## Pagos

Método                                  Endpoint                                                     Descripción 

GET                                     http://127.0.0.1:8001/api/pagos/                    Lista todos los pagos
Devuelve en formato JSON todos los pagos registrados en la base de datos.
![/assets/image-62.png](/assets/image-62.png)

POST                                    http://127.0.0.1:8001/api/pagos/                    Crea un nuevo pago
Para agregar un nuevo pago no se especifica el id dado que en los modelos implementados dejó que lo administre automáticamente el framework, los demás datos se deben especificar.
![/assets/image-63.png](/assets/image-63.png)

Al volver a hacer el GET se obtiene el pago creado junto con los anteriormente exitentes.
![/assets/image-64.png](/assets/image-64.png)

GET                                     http://127.0.0.1:8001/api/pagos/{id}/               Obtiene un pago por su ID
Para probar este EndPoint se apoya del panel de admiistración del framework para tomar un ID y obtenerlo.
![/assets/image-65.png](/assets/image-65.png)

PUT                                     http://127.0.0.1:8001/api/pagos/{id}/               Actualiza un pago por su ID
Se modifica el método de pago con el id proporcionado en este caso se modifica el pago con id = 2.
![/assets/image-66.png](/assets/image-66.png)

DELETE                                  http://127.0.0.1:8001/api/pagos/{id}/               Elimina un pago por su ID   


# Documentación de Swagger

Neuralshoes utiliza Swagger (a través de `drf-yasg`) para proporcionar una documentación interactiva de todos los endpoints de la API. Esta herramienta facilita la exploración, comprensión y prueba de los servicios REST disponibles.

## Acceso a Swagger UI

Para acceder a la interfaz de usuario de Swagger:

1. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
2. Abre en el navegador el siguiente enlace:
   ```
   http://127.0.0.1:8001/swagger/
   ```

También puedes utilizar **ReDoc** como alternativa a Swagger:
   ```
   http://127.0.0.1:8001/redoc/
   ```

## Características de la documentación con Swagger

- **Exploración visual**: Navega por todos los endpoints organizados por recursos (Clientes, Categorías, Marcas, etc.).
- **Métodos HTTP**: Cada endpoint está codificado por colores según su método (GET, POST, PUT, DELETE).
- **Parámetros**: Visualiza los parámetros requeridos y opcionales para cada endpoint.
- **Esquemas**: Revisa los esquemas de datos para entradas y salidas.
- **Pruebas interactivas**: Realiza llamadas a la API directamente desde la interfaz.

## Interfaz de Swagger en Neuralshoes

La interfaz de Swagger para Neuralshoes ofrece:

- **Panel de navegación**: Muestra todos los endpoints agrupados por recursos.
- **Sección de modelos**: Muestra los esquemas de datos de la API.
- **Área de pruebas**: Permite ejecutar solicitudes y ver respuestas en tiempo real.

## Cómo probar los endpoints desde Swagger

### Para endpoints `GET` (consulta):
1. Selecciona el endpoint que deseas probar (ej. `/api/clientes/`).
2. Haz clic en el botón **"Try it out"**.
3. Si hay parámetros opcionales, configúralos según necesites.
4. Haz clic en **"Execute"**.
5. Verás la respuesta del servidor, el código de estado HTTP y los encabezados.

### Para endpoints `POST` (creación):
1. Selecciona el endpoint `POST` (ej. `/api/productos/`).
2. Haz clic en **"Try it out"**.
3. Completa el cuerpo de la solicitud con los datos del nuevo recurso en formato JSON.
4. Haz clic en **"Execute"**.
5. Verifica en la respuesta que el recurso se ha creado correctamente.

### Para endpoints `PUT/PATCH` (actualización):
1. Selecciona el endpoint `PUT` (ej. `/api/marcas/{id}/`).
2. Ingresa el ID del recurso a actualizar.
3. Completa el cuerpo de la solicitud con los datos actualizados.
4. Haz clic en **"Execute"**.
5. Verifica que los cambios se hayan aplicado correctamente.

### Para endpoints `DELETE` (eliminación):
1. Selecciona el endpoint `DELETE` (ej. `/api/tallas/{id}/`).
2. Ingresa el ID del recurso a eliminar.
3. Haz clic en **"Execute"**.
4. Verifica que el recurso haya sido eliminado (`Código 204 No Content`).

## Ventajas de usar Swagger en el desarrollo

- **Documentación en tiempo real**: Siempre actualizada con los cambios en la API.
- **Pruebas integradas**: No requiere herramientas externas para probar endpoints.
- **Generación automática**: La documentación se genera a partir de las anotaciones en el código.
- **Facilita el desarrollo frontend**: Los desarrolladores frontend pueden entender rápidamente la estructura de la API.

## Uso de Swagger para el desarrollo front-end

Si estás desarrollando la interfaz de usuario para consumir esta API:

- Utiliza Swagger para entender la estructura de datos requerida por cada endpoint.
- Observa los códigos de respuesta posibles para manejar errores apropiadamente.
- Prueba diferentes escenarios antes de implementar las llamadas en tu código.

## Estructura de las respuestas en la API

La mayoría de los endpoints de la API de Neuralshoes siguen un formato estándar:

- **GET (colección)**: Devuelve un array de objetos.
- **GET (elemento específico)**: Devuelve un objeto único.
- **POST**: Devuelve el objeto creado con su ID asignado.
- **PUT/PATCH**: Devuelve el objeto actualizado.
- **DELETE**: No devuelve contenido (`204 No Content`).

## Autenticación en Swagger