import json
import os
from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# Definimos una función para obtener los datos del vehículo
def get_data(api_url):
    try:
        # Realizamos una petición GET a la API
        response = requests.get(api_url)
        # Convertimos la respuesta a formato JSON
        data = response.json()
        # Devolvemos los datos
        return data
    except requests.exceptions.RequestException as e:
        # En caso de error, imprimimos el error y devolvemos None
        print(f"Error obteniendo los datos: {e}")
        return None

@app.route('/connect', methods=['POST'])
def connect():
    # Guardamos la IP/puerto y el VIN en un archivo
    with open('data.json', 'w') as f:
        json.dump(request.form.to_dict(), f)
    return redirect(url_for('index'))

# Definimos la ruta principal de la aplicación
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Guardamos la IP/puerto y el VIN en un archivo
        with open('data.json', 'w') as f:
            json.dump(request.form.to_dict(), f)
        return redirect(url_for('index'))

    # Leemos la IP/puerto y el VIN del archivo
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
        ip_port = data.get('ip_port', '')
        vin = data.get('vin', '')
    else:
        ip_port = ''
        vin = ''

    if ip_port and vin:
        api_url = f"http://{ip_port}/get_vehicleinfo/{vin}?from_cache=1"
        data = get_data(api_url)
        if data:
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
                ip_port=ip_port,
                vin=vin,
                api_url=api_url,
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
            api_url = ''
            # En caso de error, renderizamos la plantilla index.html con un mensaje de error
            return render_template('index.html',
                                           error="Error obteniendo los datos. Por favor, inténtelo de nuevo más tarde.",
                                           api_url=api_url)

    else:
        # Renderizamos la plantilla index.html sin datos
        return render_template('index.html')

# Comprobamos si el script se está ejecutando directamente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port)
