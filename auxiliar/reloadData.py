from flask import url_for, redirect
from auxiliar import utilidades, sesion
from auxiliar.data import save_to_historical_data


def recargarPaginatimer():

    vin_coche = sesion.session.get_vin()
    ip_port = sesion.session.get_ip_port()

    if vin_coche and ip_port:
        api_url = utilidades.construirAPI(ip_port, vin_coche)
        data = utilidades.get_data(api_url)
        if data:
            save_to_historical_data(data)
        return redirect(url_for('index'))


def tarea_programada():
    recargarPaginatimer()
    print("Tarea ejecutada")
