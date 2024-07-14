# Guía de Instalación de SensorStats en Docker

## Requisitos Previos

1. Asegúrate de tener Docker instalado en tu sistema.
2. Crea una cuenta en [Docker Hub](https://hub.docker.com).

## Pasos de Instalación

### 1. Buscar la Imagen en Docker Hub

- Ingresa a [Docker Hub](https://hub.docker.com) y busca la imagen `fletsv/sensorstatsamd64`.

### 2. Clonar la Imagen

- Desde el gestor cliente de Docker o la línea de comandos, clona la imagen:


docker pull fletsv/sensorstatsamd64

### 3. Crear Carpetas y Archivos Necesarios

- Crea una carpeta `data` donde desees almacenar tus datos.
- Dentro de la carpeta `data`, crea dos archivos:
  - `historical_data.json`
  - `data.json`

### 4. Ejecutar la Imagen desde la Línea de Comandos

- Ejecuta el siguiente comando para poner en marcha el contenedor:


`docker run -d --name sensorstats -p 5006:8080 -e TZ=Europe/Madrid -v $(pwd)/data:/app/data/historialDatos fletsv/sensorstatsamd64`

### 5. Ejecutar la Imagen desde el Gestor Cliente de Docker

- Abre el gestor cliente de Docker.
- Selecciona la opción para ejecutar o iniciar la imagen.
- Asigna un nombre al contenedor, por ejemplo, `sensorstats`.
- Añade el puerto del contenedor: `5006` en el host y `8080` en el contenedor.
- Mapea la carpeta `data` dentro del contenedor en volumen y dentro del contenedor como `/app/data/historialDatos`.
- Inicia el contenedor.

## Acceso a la Aplicación

- Una vez iniciado el contenedor, puedes acceder a la aplicación a través de `http://localhost:5006`.

## Configuración Inicial

- Si es la primera vez que abres el programa, deberás configurar la dirección y el VIM correspondiente desde `psaCarController`.
- Esta configuración se almacenará para futuros usos.

¡Y eso es todo! Ahora deberías tener `SensorStats` funcionando en tu contenedor Docker.

