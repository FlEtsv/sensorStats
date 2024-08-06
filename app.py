import atexit
import json
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler

from auxiliar.Api.conexion import api_cn
from auxiliar.Api.get_datos import api_bp
import auxiliar
from flask import Flask, jsonify, request, redirect, url_for, render_template

from auxiliar import sesion
from auxiliar.action import evaluar, evaluarIndex
from auxiliar.data import get_data, save_to_historical_data, get_historical_data, get_data_boolean
from auxiliar.manipulacionDatos.sqlite import create_database, guardarDatosWeb
from auxiliar.reloadData import tarea_programada

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(api_bp)
app.register_blueprint(api_cn)


@app.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        bot_name = request.form['name']
        bot_token = request.form['token']
        phone_number = request.form['Numero']
        create_database()
        # Save the bot configuration to a sqlite database
        codigoVerificacion = guardarDatosWeb(bot_name, bot_token, phone_number)

        # Redirect to a success page or render a template
        return redirect(url_for('success', codigoVerificacion=codigoVerificacion))

    return render_template('BotDisplay.html')

@app.route('/success/<codigoVerificacion>')
def success(codigoVerificacion):
    return render_template('success.html', codigoVerificacion=codigoVerificacion)

@app.route('/configuracionBot')
def configuracionBot():
    return render_template('BotDisplay.html')

# Ruta para mostrar los últimos registros de un dato específico
@app.route('/data/<data_type>')
def show_data(data_type):
    data = get_historical_data(data_type)

    # Si el data_type es 'voltaje', multiplica cada valor por cuatro
    if data_type == 'battery_voltage':
        for entry in data:
            entry['value'] *= 4
    #vamos a pasar cada valor de la lista por el metodo que lo evalua y nos devuelve el color de la celda de la lista que tendra que tener
    for entry in data:
        entry['color'] = evaluar(entry['value'], data_type)

    return render_template('data.html', data=data, data_type=data_type)


@app.route('/connect', methods=['POST'])
def connect():
    file_path = 'data/historialDatos/data.json'
    try:
        # Log the request form data
        print(f"Request form data: {request.form}")
        # Log the sesion updates
        vin = request.form['vin']
        ip_port = request.form['ip_port']

        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if get_data_boolean(auxiliar.utilidades.construirAPI(ip_port, vin)):
            # Save the connection data to data.json
            with open(file_path, 'w') as f:
                json.dump(request.form.to_dict(), f)
            sesion.sesion.get_instance().set_vin(vin)
            sesion.sesion.get_instance().set_ip_port(ip_port)

            # guardar estos datos en el json
            return redirect(url_for('index_get')), 302
        else:
            vin = ''
            ip_port = ''
            sesion.sesion.get_instance().set_vin(vin)
            sesion.sesion.get_instance().set_ip_port(ip_port)
            return redirect(url_for('index_get')), 302



        print(f"Setting sesion VIN: {vin}")
        print(f"Setting sesion IP/Port: {ip_port}")

    except Exception as e:
        print(f"Error in connect route: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Error saving data: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index_get():
    file_path = 'data/historialDatos/data.json'

    # Ensure the directory exists before reading the file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Initialize data
    data = {}

    # Check if the file exists
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f)
    else:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logging.error("Error decoding data.json")
            return jsonify({"error": "Error obteniendo los datos"}), 200

    ip_port = data.get('ip_port', '')
    vin = data.get('vin', '')
    sesion.sesion.get_instance().clear()
    sesion.sesion.get_instance().set_ip_port(ip_port)
    sesion.sesion.get_instance().set_vin(vin)

    # Initialize default variables
    battery_voltage = 0
    autonomy = 0
    charging_mode = "N/A"
    charging_status = "N/A"
    level = 0
    air_temp = 0
    luminosity_day = False
    acceleration = 0
    speed = 0
    preconditioning_status = "N/A"
    mileage = 0
    coordinates = [0, 0]
    error = None
    api_url = ''

    if ip_port and vin:
        if get_data_boolean(auxiliar.utilidades.construirAPI(ip_port, vin)):
            api_url = f"http://{ip_port}/get_vehicleinfo/{vin}?from_cache=1"
            data = get_data(api_url)
            if data:
                try:
                    last_position = data.get('last_position', {}).get('geometry', {}).get('coordinates', [0, 0])
                    coordinates = [last_position[1], last_position[0]]  # Leaflet uses [lat, lon]
                    battery_voltage = data.get('battery', {}).get('voltage', 0)
                    energy = data.get('energy', [{}])[0]
                    autonomy = energy.get('autonomy', 0)
                    charging = energy.get('charging', {})
                    charging_mode = charging.get('charging_mode', "N/A")
                    charging_status = charging.get('status', "N/A")
                    level = energy.get('level', 0)
                    environment = data.get('environment', {})
                    air_temp = environment.get('air', {}).get('temp', 0)
                    luminosity_day = environment.get('luminosity', {}).get('day', False)
                    kinetic = data.get('kinetic', {})
                    acceleration = kinetic.get('acceleration', 0)
                    speed = kinetic.get('speed', 0)
                    preconditioning = data.get('preconditionning', {}).get('air_conditioning', {})
                    preconditioning_status = preconditioning.get('status', "N/A")
                    mileage = data.get('timed_odometer', {}).get('mileage', 0)

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
                except Exception as e:
                    logging.error(f"Error in data representation: {e}")
                    return jsonify({"error": "Error obteniendo los datos"}), 200
            else:
                error = "Error obteniendo los datos."
                return jsonify({"error": "Error obteniendo los datos"}), 200
        else:
            error = "Error obteniendo los datos."
            return jsonify({"error": "Error obteniendo los datos"}), 200
    else:
        error = "Error obteniendo los datos."
        return jsonify({"error": f" Error obteniendo los datos"}), 200

    colorBV = evaluarIndex(battery_voltage, 'battery_voltage')
    colorAutonomy = evaluarIndex(autonomy, 'autonomy')
    colorAirTemp = evaluarIndex(air_temp, 'air_temp')
    colorLevel = evaluarIndex(level, 'level')
    colorLD = evaluarIndex(luminosity_day, 'luminosity_day')
    colorPS = evaluarIndex(preconditioning_status, 'preconditioning_status')
    colorCargando = evaluarIndex(charging_status, 'charging_status')
    colorModoCarga = evaluarIndex(charging_mode, 'charging_mode')

    return render_template(
        'index.html',
        ip_port=ip_port,
        vin=vin,
        api_url=api_url,
        battery_voltage=battery_voltage,
        colorBV=colorBV,
        autonomy=autonomy,
        colorAutonomy=colorAutonomy,
        charging_mode=charging_mode,
        colorModoCarga=colorModoCarga,
        charging_status=charging_status,
        colorCargando=colorCargando,
        level=level,
        colorLevel=colorLevel,
        air_temp=air_temp,
        colorAirTemp=colorAirTemp,
        luminosity_day=luminosity_day,
        colorLD=colorLD,
        acceleration=acceleration,
        speed=speed,
        preconditioning_status=preconditioning_status,
        colorPS=colorPS,
        mileage=mileage,
        error=error,
        coordinates=coordinates,
        version='1.3.8'
    ), 200

@app.route('/', methods=['POST'])
def index_post():
    file_path = 'data/historialDatos/data.json'

    # Asegurarse de que el directorio existe antes de escribir el archivo
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Guardar los datos de conexión en data.json
    try:
        with open(file_path, 'w') as f:
            json.dump(request.form.to_dict(), f)
    except Exception as e:
        logging.error(f"Error escribiendo data.json: {e}")
        return jsonify({"error": "Error guardando los datos"}), 200

    sesion.sesion.get_instance().set_vin(request.form['vin'])
    sesion.sesion.get_instance().set_ip_port(request.form['ip_port'])
    return redirect(url_for('index')), 302


# Inicializar el planificador de fondo
scheduler = BackgroundScheduler()
scheduler.add_job(func=tarea_programada, trigger="interval", hours=3)
scheduler.start()

# Apagar el planificador cuando se cierre la aplicación
atexit.register(scheduler.shutdown)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port)