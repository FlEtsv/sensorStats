# Importamos las librerías necesarias
from flask import Flask, render_template
import requests

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Definimos una función para obtener los datos del vehículo
def get_data():
    # URL de la API desde la que obtenemos los datos
    url = "http://192.168.1.16:5005/get_vehicleinfo/VR3UHZKXZPT573301?from_cache=1"
    # URL de la API desde la que obtenemos los datos
    #"http://192.168.1.16:5005/get_vehicleinfo/VR3UHZKXZPT573301?from_cache=1"
    try:
        # Realizamos una petición GET a la API
        response = requests.get(url)
        # Convertimos la respuesta a formato JSON
        data = response.json()
        # Devolvemos los datos
        return data
    except requests.exceptions.RequestException as e:
        # En caso de error, imprimimos el error y devolvemos None
        print(f"Error obteniendo los datos: {e}")
        return None

# Definimos la ruta principal de la aplicación
@app.route('/')
def index():
    # Obtenemos los datos del vehículo
    data = get_data()
    if data:
        # Extraemos los datos necesarios del JSON
        battery_voltage = data.get('battery', {}).get('voltage')
        energy = data.get('energy', [{}])[0]
        autonomy = energy.get('autonomy')
        charging = energy.get('charging', {})
        charging_mode = charging.get('charging_mode')
        charging_status = charging.get('status')
        level = energy.get('level')
        environment = data.get('environment', {})
        air_temp = environment.get('air', {}).get('temp')
        luminosity_day = environment.get('luminosity', {}).get('day')
        kinetic = data.get('kinetic', {})
        acceleration = kinetic.get('acceleration')
        speed = kinetic.get('speed')
        preconditioning = data.get('preconditionning', {}).get('air_conditioning', {})
        preconditioning_status = preconditioning.get('status')
        mileage = data.get('timed_odometer', {}).get('mileage')

        # Renderizamos la plantilla index.html con los datos obtenidos
        return render_template(
            'index.html',
            battery_voltage=battery_voltage,
            autonomy=autonomy,
            charging_mode=charging_mode,
            charging_status=charging_status,
            level=level,
            air_temp=air_temp,
            luminosity_day=luminosity_day,
            acceleration=acceleration,
            speed=speed,
            preconditioning_status=preconditioning_status,
            mileage=mileage
        )
    else:
        # En caso de error, renderizamos la plantilla index.html con un mensaje de error
        return render_template('index.html', error="Error obteniendo los datos. Por favor, inténtelo de nuevo más tarde.")

# Comprobamos si el script se está ejecutando directamente
if __name__ == '__main__':
    # En caso afirmativo, ejecutamos la aplicación
    app.run(host='0.0.0.0', port=8080)