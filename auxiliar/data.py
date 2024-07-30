import datetime
import json
import os

import requests


import requests

def get_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def get_data_boolean(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return False

def save_to_historical_data(data):
    historical_data = []

    # Verificar si existe el archivo, si no, crearlo vacío
    if not os.path.exists('data/historialDatos/historical_data.json'):
        with open('data/historialDatos/historical_data.json', 'w') as f:
            json.dump(historical_data, f)

    # Cargar los datos históricos existentes
    with open('data/historialDatos/historical_data.json', 'r') as f:
        try:
            historical_data = json.load(f)
        except json.JSONDecodeError:
            print("Error decodificando historical_data.json")
            historical_data = []

    # Verificar si los nuevos datos son únicos antes de agregarlos
    new_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'data': data
    }

    # Verificar duplicados considerando fecha y hora
    new_data_datetime = datetime.datetime.fromisoformat(new_data['timestamp'])
    for entry in historical_data:
        entry_datetime = datetime.datetime.fromisoformat(entry['timestamp'])
        # Compara hasta minutos para evitar duplicados en el mismo minuto
        if entry_datetime.strftime('%Y-%m-%d %H:%M') == new_data_datetime.strftime('%Y-%m-%d %H:%M'):
            # Si ya existe una entrada para la misma fecha y hora, comparamos el contenido
            if entry['data'] == new_data['data']:
                return  # No se agrega duplicado

    # Agregar los nuevos datos a la lista histórica
    historical_data.append(new_data)

    # Eliminar los registros más antiguos si hay más de 50
    if len(historical_data) > 50:
        # Ordenar por fecha para asegurar que se eliminen los más antiguos
        historical_data.sort(key=lambda x: datetime.datetime.fromisoformat(x['timestamp']))
        # Mantener solo los 50 más recientes
        historical_data = historical_data[-50:]

    # Guardar los datos actualizados en el archivo
    with open('data/historialDatos/historical_data.json', 'w') as f:
        json.dump(historical_data, f)


def get_historical_data(data_type):
    historical_data = []

    if os.path.exists('data/historialDatos/historical_data.json'):
        with open('data/historialDatos/historical_data.json', 'r') as f:
            try:
                historical_data = json.load(f)
            except json.JSONDecodeError:
                print("Error decodificando historical_data.json")
                historical_data = []

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

#metodo que accede a data.json que esta en data/historialDatos/data.json y obtiene el ip_port y vin