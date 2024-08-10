
import json
import logging
import os
import time

from flask import Flask, jsonify, request, redirect, url_for, render_template, Blueprint, make_response, \
    send_from_directory

import auxiliar
from auxiliar import sesion, reloadData
from auxiliar.Api.conexion import api_cn
from auxiliar.Api.configuracionBot import api_cb
from auxiliar.Api.get_datos import api_bp
from auxiliar.action import evaluar
from auxiliar.data import save_to_historical_data, get_historical_data, get_data_boolean, \
    obtenerTimestampsMasReciente
from auxiliar.indexBack.indexBack import read_data_from_file, set_session_data, initialize_default_variables, \
    fetch_and_process_vehicle_data, render_index_template, preparativos
from bot.botView import bot_v

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(api_cn)
app.register_blueprint(api_cb)
app.register_blueprint(api_bp)

app.register_blueprint(bot_v)



@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.cache_control.max_age = 3600  # Cache static files for 1 hour
    return response

@app.route('/static/<path:filename>')
def static_files(filename):
    response = make_response(send_from_directory('static', filename))
    response.cache_control.max_age = 3600  # Cache static files for 1 hour
    return response

# app.py
@app.route('/data/<data_type>')
def show_data(data_type):
    data = get_historical_data(data_type)
    if data_type == 'battery_voltage':
        for entry in data:
            entry['value'] *= 4
    for entry in data:
        entry['color'] = evaluar(entry['value'], data_type)
    return render_template('data.html', data=data, data_type=data_type)

@app.route('/connect', methods=['POST'])
def connect():
    file_path = 'data/historialDatos/data.json'
    try:
        vin = request.form['vin']
        ip_port = request.form['ip_port']
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if get_data_boolean(auxiliar.reloadData.utilidades.construirAPI(ip_port, vin)):
            with open(file_path, 'w') as f:
                json.dump(request.form.to_dict(), f)
            sesion_instance = sesion.sesion.get_instance()
            sesion_instance.set_vin(vin)
            sesion_instance.set_ip_port(ip_port)
            return redirect(url_for('index_get')), 302
        else:
            sesion_instance = sesion.sesion.get_instance()
            sesion_instance.clear()  # Clear only if data fetch fails
            return redirect(url_for('index_get')), 302
    except Exception as e:
        logging.error(f"Error in connect route: {e}")
        return jsonify({"error": f"Error saving data: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index_get():
    file_path = 'data/historialDatos/data.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = read_data_from_file(file_path)
    ip_port, vin = set_session_data(data)
    context = initialize_default_variables()
    context.update({'ip_port': ip_port, 'vin': vin})
    if not ip_port or not vin:
        return render_index_template(context)
    vehicle_data = fetch_and_process_vehicle_data(ip_port, vin)
    if vehicle_data:
        context.update(vehicle_data)
    else:
        context['error'] = "Error obteniendo los datos."

    ultimaActualizacion = obtenerTimestampsMasReciente()
    return render_index_template(context,ultimaActualizacion)

@app.route('/', methods=['POST'])
def index_post():
    file_path = 'data/historialDatos/data.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w') as f:
            json.dump(request.form.to_dict(), f)
    except Exception as e:
        logging.error(f"Error escribiendo data.json: {e}")
        return jsonify({"error": "Error guardando los datos"}), 200
    sesion.sesion.get_instance().set_vin(request.form['vin'])
    sesion.sesion.get_instance().set_ip_port(request.form['ip_port'])
    return redirect(url_for('index')), 302




if __name__ == '__main__':
    preparativos()
    reloadData.ReloadData().initReload()
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port, debug=True)
