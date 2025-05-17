# Usa una imagen base de Python
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del backend
COPY . /app

# Expone el puerto 8000 para acceder a Django
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py poblar_db && python manage.py runserver 0.0.0.0:8000"]