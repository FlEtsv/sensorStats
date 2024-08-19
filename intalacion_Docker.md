# Guía de Instalación de SensorStats en Docker

## Requisitos Previos

1. Asegúrate de tener Docker instalado en tu sistema.
2. Crea una cuenta en [Docker Hub](https://hub.docker.com).

## Pasos de Instalación

### 1. Buscar la Imagen en Docker Hub

- Ingresa a [Docker Hub](https://hub.docker.com) y busca la imagen `fletsv/sensorstatsamd64`.

### 2. Clonar la Imagen

- Desde el gestor cliente de Docker o la línea de comandos, clona la imagen:


`docker pull fletsv/sensorstatsamd64`

### 3. Crear Carpetas Necesarias
Esta carpeta serviran a la apliacion de almacenamiento.
- Crea una carpeta `data` donde desees almacenar tus datos(en el sitema operativo)


### 4. Ejecutar la Imagen desde la Línea de Comandos

- Ejecuta el siguiente comando para poner en marcha el contenedor:

`docker run -d --name sensorstats -p {Puertodeseado}:8080 -e TZ=Europe/Madrid -v $(pwd)/data:/app/data/historialDatos fletsv/sensorstatsamd64`


### 5. Ejecutar la Imagen desde el Gestor Cliente de Docker

- Abre el gestor cliente de Docker.
- Selecciona la opción para ejecutar o iniciar la imagen.
- Asigna un nombre al contenedor, por ejemplo, `sensorstats`.
- Añade el puerto del contenedor: `puertoDeseado` en el host y `8080` en el contenedor.
- Mapea la carpeta `data` (la que creaste anteriormente)dentro del contenedor en volumen y dentro del contenedor como `/app/data/historialDatos`.
- Inicia el contenedor.

  ⚠️ WARNING: si va a instalar el bot de telegram necesitara el conjunto de rutas marcadas anteriormenta para el bot

## Acceso a la Aplicación

- Una vez iniciado el contenedor, puedes acceder a la aplicación a través de `http://localhost:{Puerto}`.

## Configuración Inicial

- Si es la primera vez que abres el programa, deberás configurar la dirección y el VIM correspondiente desde `psaCarController` correspondiente a la instalación de docker en "https://github.com/flobz/psa_car_controller". si se encuentra alojado en la misma ip solo debera poner el puerto de la instalación. Seguir "https://github.com/flobz/psa_car_controller/blob/master/docs/Docker.md" para tener los controladores y instalar el mio para visualizar los datos  a detalle y historiales.
- Esta configuración se almacenará para futuros usos.


## Avisos y configuracion de bot Telegram.
  el bot de telegram necesita esta instalación para funcionar, el bot de telegram funciona en cualquier parte del mundo, pero es seguro porque verifica siempre el Chat.Id que esta verificado, por     lo tanto solo usted "USUARIO VERIFICADO" podrá acceder al contenido del mismo.
  ¡Y eso es todo! Ahora deberías tener `SensorStats` funcionando en tu contenedor Docker.
