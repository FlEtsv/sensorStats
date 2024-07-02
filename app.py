import json
import os
from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Función para obtener datos históricos de un tipo específico
def get_historical_data(data_type):
    historical_data = []

    if os.path.exists('historical_data.json'):
        with open('historical_data.json', 'r') as f:
            historical_data = json.load(f)

    # Filtrar datos por el tipo especificado y tomar los últimos 50 registros
    filtered_data = []
    count = 0
    for entry in reversed(historical_data):
        if count >= 50:
            break
        if data_type in entry['data']:
            filtered_data.append({
                'timestamp': entry['timestamp'],
                'value': entry['data'][data_type]
            })
            count += 1

    return filtered_data


# Ruta para mostrar los últimos registros de un dato específico
@app.route('/data/<data_type>')
def show_data(data_type):
    data = get_historical_data(data_type)
    return render_template('data.html', data=data, data_type=data_type)


def get_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza un error HTTP si la respuesta no es exitosa

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error obteniendo los datos: {e}")
        return None


def save_to_historical_data(data):
    historical_data = []

    if os.path.exists('historical_data.json'):
        with open('historical_data.json', 'r') as f:
            historical_data = json.load(f)

    # Verificar si los nuevos datos son únicos antes de agregarlos
    new_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'data': data
    }

    # Verificar duplicados
    for entry in historical_data:
        if entry['timestamp'].split('T')[0] == new_data['timestamp'].split('T')[0]:
            # Si ya existe una entrada para la misma fecha, comparamos el contenido
            if entry['data'] == new_data['data']:
                return  # No se agrega duplicado

    # Agregar los nuevos datos a la lista histórica
    historical_data.append(new_data)

    with open('historical_data.json', 'w') as f:
        json.dump(historical_data, f)


@app.route('/connect', methods=['POST'])
def connect():
    with open('data.json', 'w') as f:
        json.dump(request.form.to_dict(), f)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        with open('data.json', 'w') as f:
            json.dump(request.form.to_dict(), f)
        return redirect(url_for('index'))

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
            try:
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

                # Guardar datos en historical_data.json
                save_to_historical_data({
                    'battery_voltage': battery_voltage,
                    'autonomy': autonomy,
                    'charging_mode': charging_mode,
                    'charging_status': charging_status,
                    'level': level,
                    'air_temp': air_temp,
                    'luminosity_day': luminosity_day,
                    'acceleration': acceleration,
                    'speed': speed,
                    'preconditioning_status': preconditioning_status,
                    'mileage': mileage
                })

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
            except Exception as e:
                print(f"Error en la representación de los datos: {e}")
                return render_template('index.html',
                                       error="Error en la representación de los datos. Por favor, inténtelo de nuevo más tarde.",
                                       api_url=api_url)
        else:
            api_url = ''
            return render_template('index.html',
                                   error="Error obteniendo los datos. Por favor, inténtelo de nuevo más tarde.",
                                   api_url=api_url)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port)
