import atexit
import atexit
import json
import logging
import os
import threading
import time

from flask import Flask, jsonify, request, redirect, url_for, render_template

import auxiliar
from auxiliar import sesion
from auxiliar.action import evaluar, evaluarIndex
from auxiliar.data import get_data, save_to_historical_data, get_historical_data, get_data_boolean, \
    obtenerTimestampsMasReciente
from auxiliar.indexBack.indexBack import read_data_from_file, set_session_data, initialize_default_variables, \
    fetch_and_process_vehicle_data, render_index_template
from auxiliar.manipulacionDatos.sqlite import create_database, guardarDatosWeb
from auxiliar.reloadData import tarea_programada, run_periodic_task, initReload

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        bot_name = request.form['name']
        bot_token = request.form['token']
        phone_number = request.form['Numero']
        create_database()
        codigoVerificacion = guardarDatosWeb(bot_name, bot_token, phone_number)
        return redirect(url_for('success', codigoVerificacion=codigoVerificacion))
    return render_template('BotDisplay.html')

@app.route('/success/<codigoVerificacion>')
def success(codigoVerificacion):
    return render_template('success.html', codigoVerificacion=codigoVerificacion)

@app.route('/configuracionBot')
def configuracionBot():
    return render_template('BotDisplay.html')

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
            sesion.sesion.get_instance().set_vin(vin)
            sesion.sesion.get_instance().set_ip_port(ip_port)
            return redirect(url_for('index_get')), 302
        else:
            vin = ''
            ip_port = ''
            sesion.sesion.get_instance().set_vin(vin)
            sesion.sesion.get_instance().set_ip_port(ip_port)
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
    initReload()
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port, debug=True)