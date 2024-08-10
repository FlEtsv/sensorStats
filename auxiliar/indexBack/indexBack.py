import json
import logging
import os

from flask import render_template

from auxiliar.action import evaluarIndex
from auxiliar.data import get_data, save_to_historical_data
from auxiliar.sesion import sesion


def initialize_data():
    return {}

def read_data_from_file(file_path):
    data = {}
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logging.error("Error decoding data.json")
            data = {}
    return data

# indexBack.py
def set_session_data(data):
    ip_port = data.get('ip_port', '')
    vin = data.get('vin', '')
    sesion_instance = sesion.get_instance()
    sesion_instance.set_ip_port(ip_port)
    sesion_instance.set_vin(vin)
    #depuracion para saber si se esta guardando correctamente
    logging.debug(f"ip_port: {sesion_instance.get_ip_port()}")
    logging.debug(f"vin: {sesion_instance.get_vin()}")


    return ip_port, vin

def preparativos():

    data = read_data_from_file('data/historialDatos/data.json')
    if data:

        ip_port, vin = set_session_data(data)
    else:
         logging.debug("no datos")
    logging.debug("Preparativos completados")



def initialize_default_variables():
    return {
        'battery_voltage': 0,
        'autonomy': 0,
        'charging_mode': "N/A",
        'charging_status': "N/A",
        'level': 0,
        'air_temp': 0,
        'luminosity_day': False,
        'acceleration': 0,
        'speed': 0,
        'preconditioning_status': "N/A",
        'mileage': 0,
        'coordinates': [0, 0],
        'error': None,
        'api_url': ''
    }

def fetch_and_process_vehicle_data(ip_port, vin):
    api_url = f"http://{ip_port}/get_vehicleinfo/{vin}?from_cache=1"

    data = get_data(api_url)
    if data:
        try:
            sesion_instance = sesion.get_instance()
            sesion_instance.set_vin(vin)
            sesion_instance.set_ip_port(ip_port)
            return extract_vehicle_data(data)
        except Exception as e:
            logging.error(f"Error in data representation: {e}")
            return None
    return None

def render_index_template(context, ultimaActualizacion=None):
    return render_template(
        'index.html',
        ip_port=context['ip_port'],
        vin=context['vin'],
        api_url=context['api_url'],
        battery_voltage=context['battery_voltage'],
        colorBV=evaluarIndex(context['battery_voltage'], 'battery_voltage'),
        autonomy=context['autonomy'],
        colorAutonomy=evaluarIndex(context['autonomy'], 'autonomy'),
        charging_mode=context['charging_mode'],
        colorModoCarga=evaluarIndex(context['charging_mode'], 'charging_mode'),
        charging_status=context['charging_status'],
        colorCargando=evaluarIndex(context['charging_status'], 'charging_status'),
        level=context['level'],
        colorLevel=evaluarIndex(context['level'], 'level'),
        air_temp=context['air_temp'],
        colorAirTemp=evaluarIndex(context['air_temp'], 'air_temp'),
        luminosity_day=context['luminosity_day'],
        colorLD=evaluarIndex(context['luminosity_day'], 'luminosity_day'),
        acceleration=context['acceleration'],
        speed=context['speed'],
        preconditioning_status=context['preconditioning_status'],
        colorPS=evaluarIndex(context['preconditioning_status'], 'preconditioning_status'),
        mileage=context['mileage'],
        error=context['error'],
        coordinates=context['coordinates'],
        version='1.4.3',
        ultimaActualizacion=ultimaActualizacion

    ), 200


def extract_vehicle_data(data):
    last_position = data.get('last_position', {}).get('geometry', {}).get('coordinates', [0, 0])
    coordinates = [last_position[1], last_position[0]]
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

    return {
        'coordinates': coordinates,
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
    }