# sensorStats 📅

## Descripción

El proyecto PsaCarController está diseñado para mostrar datos de sensores de vehículos en una instalación de Docker. Proporciona información interesante y útil para los usuarios finales mediante una interfaz web atractiva y moderna.

## Estructura del Proyecto

- `app.py`: Es una instancia del servidor Flask. Este archivo se encarga de recuperar los datos en formato JSON desde la API de psaCarController, procesarlos y enviarlos a la plantilla para su visualización.
- `index.html`: Es una plantilla diseñada para mostrar los datos al usuario final. Utiliza gráficos para construir visualizaciones y representar la información de manera efectiva.

## Uso

La aplicación recupera datos de sensores del vehículo desde la API de psaCarController y los presenta en gráficos circulares y otros elementos visuales en la página web. La página se actualiza automáticamente cada hora para mostrar la información más reciente.

## Estructura del Código

- `app.py`: Este archivo contiene el servidor Flask que realiza las siguientes tareas:
  - Recupera datos en formato JSON desde la API de psaCarController.
  - Procesa los datos y los prepara para la visualización.
  - Renderiza la plantilla index.html con los datos procesados.
- `index.html`: Esta plantilla presenta los datos al usuario final utilizando cards con imagenes y el valor. Los cards incluyen:
  - Voltaje de la batería
  - Autonomía
  - Nivel de la batería
  - Temperatura del aire
  - Aceleración
  - Velocidad
  - Kilometraje
  - Modo de carga
  - Estado de carga
  - Luminosidad del día
  - Estado del preacondicionamiento
- `data.html`: Esta plantilla presenta los datos mas a detalle, nos muestra una tabla que nos facilita el formato Fecha-Valor, asi como un grafico de barras para poder ver visualmente la evolucion.
- `BotDisplay.html`: Esta plantilla es la presentación y configuracion del Bot.
- 

## Tecnologías Utilizadas

- Flask: Microframework para Python que facilita la creación de aplicaciones web.
- Docker: Plataforma para desarrollar, enviar y ejecutar aplicaciones en contenedores.
- Chart.js: Biblioteca de JavaScript para crear gráficos atractivos y personalizables.


## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork de este repositorio.
2. Crea una rama nueva (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.
