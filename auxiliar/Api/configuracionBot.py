from email.quoprimime import unquote

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from auxiliar.manipulacionDatos.BD.repository import MetodosDatabase

api_cb = Blueprint('api_cb', __name__)
db_methods = MetodosDatabase()

@api_cb.route('/api/configBot', methods=['POST'])
def config_bot():
    db_methods.create_database_config()

    voltaje = request.form.get('voltaje_active') is not None
    bateria = request.form.get('bateria_active') is not None
    temperatura = request.form.get('temperatura_active') is not None
    autonomia = request.form.get('autonomia_active') is not None
    kilometraje = request.form.get('kilometraje_active') is not None

    if not (voltaje or bateria or temperatura or autonomia or kilometraje):
        print("ninguna notificacion marcada")
        return dialogoWarningVacio(), 200

    if voltaje:
        print("Voltaje marcado")
        voltaje_value = request.form.get('voltaje_valor')
        if voltaje_value is None:
            return dialogowarningRequired("voltaje"), 200
        try:
            float(voltaje_value)
        except ValueError:
            return dialogoWarninFormatError("voltaje"), 200

    if bateria:
        print("Bateria marcada")
        bateria_value = request.form.get('bateria_valor')
        if bateria_value is None:
            return dialogowarningRequired("bateria"), 200
        try:
            float(bateria_value)
        except ValueError:
            return dialogoWarninFormatError("bateria"), 200

    if temperatura:
        print("Temperatura marcada")
        temperatura_value = request.form.get('temperatura_valor')
        if temperatura_value is None:
            return dialogowarningRequired("temperatura"), 200
        try:
            float(temperatura_value)
        except ValueError:
            return dialogoWarninFormatError("temperatura"), 200

    if autonomia:
        print("Autonomia marcada")
        autonomia_value = request.form.get('autonomia_valor')
        if autonomia_value is None:
            return dialogowarningRequired("autonomia"), 200
        try:
            float(autonomia_value)
        except ValueError:
            return dialogoWarninFormatError("autonomia"), 200

    if kilometraje:
        print("Kilometraje marcado")
        kilometraje_value = request.form.get('kilometraje_valor')
        if kilometraje_value is None:
            return dialogowarningRequired("kilometraje"), 200
        try:
            float(kilometraje_value)
        except ValueError:
            return dialogoWarninFormatError("kilometraje"), 200

    return dialogoTodoCorrecto(), 200

@api_cb.route('/dialog/<tipoAviso>/<mensajeUsuario>', methods=['GET'])
def dialog(tipoAviso, mensajeUsuario):
    tipoAviso = unquote(tipoAviso)
    mensajeUsuario = unquote(mensajeUsuario)
    return render_template('configBotDialog.html', tipoAviso=tipoAviso, mensajeUsuario=mensajeUsuario)

def dialogoTodoCorrecto():
    return llevarDialogo("Enhorabuena", "Configuracion guardada correctamente")

def dialogoWarningVacio():
    return llevarDialogo("Cuidado!", "Ninguna notificacion marcada")

def dialogowarningRequired(nombre):
    return llevarDialogo("Cuidado!", f"Valor nulo para {nombre}")

def dialogoWarninFormatError(nombre):
    return llevarDialogo("Cuidado!", f"Valor invalido para {nombre}")

def llevarDialogo(tipoAviso, mensajeUsuario):
    return render_template('configBotDialog.html', tipoAviso=tipoAviso, mensajeUsuario=mensajeUsuario)
