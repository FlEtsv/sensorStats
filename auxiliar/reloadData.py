from flask import url_for, redirect
from auxiliar import utilidades, sesion
from auxiliar.data import save_to_historical_data


def recargarPaginatimer():
    return redirect(url_for('index'))


def tarea_programada():
    recargarPaginatimer()
    print("Tarea ejecutada")
