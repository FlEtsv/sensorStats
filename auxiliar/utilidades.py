import string



def construirAPI(ip_port, vin):
    return f"http://{ip_port}/get_vehicleinfo/{vin}?from_cache=1"