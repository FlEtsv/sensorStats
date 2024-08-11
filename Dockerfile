# Usa una imagen base de Python
FROM python:3.9-slim

# Establece la zona horaria
ENV TZ=Europe/Madrid

# Instala dependencias del sistema para cambiar la zona horaria
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt



# Expone el puerto que la aplicación usará
EXPOSE 8080

# Define el comando por defecto para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]