from flask import Flask, render_template, request, redirect, url_for, session
import requests

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

# Definimos la ruta principal de la aplicación
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Guardamos la URL de la API en la sesión
        session['api_url'] = request.form['api_url']
        return redirect(url_for('index'))

    # Obtenemos la URL de la API de la sesión
    api_url = session.get('api_url', "http://192.168.1.16:5005/get_vehicleinfo/VR3UHZKXZPT573301?from_cache=1")
    data = get_data(api_url)
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
        # En caso de error, renderizamos la plantilla index.html con un mensaje de error
        return render_template('index.html', error="Error obteniendo los datos. Por favor, inténtelo de nuevo más tarde.", api_url=api_url)

# Comprobamos si el script se está ejecutando directamente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
