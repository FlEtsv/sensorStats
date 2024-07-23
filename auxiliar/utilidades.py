import string

from auxiliar import sesion


def construirAPI(ip_port, vin):
    return f"http://{ip_port}/get_vehicleinfo/{vin}?from_cache=1"

def sacarCoordenadas(data):
    if data:
        try:
            coordenadas = data.get('location', {}).get('coordinates', [])
            if coordenadas:
                return coordenadas
        except Exception as e:
            print(f"Error sacando coordenadas: {e}")

    return [], sesion.session.get_instance().set_coordenadas([])