# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto que la aplicación usará
EXPOSE 8080

# Define el comando por defecto para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:${PORT:-5006}", "app:app"]
