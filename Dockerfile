# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del backend
COPY / .

# Expone el puerto 8000 para acceder a Django
EXPOSE 8000

# Comando para ejecutar el servidor de Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]