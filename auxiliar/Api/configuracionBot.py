from email.quoprimime import unquote

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from auxiliar.manipulacionDatos.BD.repository import MetodosDatabase


api_cb = Blueprint('api_cb', __name__)

db_methods = MetodosDatabase()

@api_cb.route('/api/configBot', methods=['POST'])
def config_bot():


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
        intVoltaje = int(voltaje_value)
        if voltaje_value is None:
            return dialogowarningRequired("voltaje"), 200
        db_methods.eliminarDatosConfig("voltaje")
        db_methods.guardarDatoConfig("voltaje", intVoltaje, True)
        try:
            float(voltaje_value)
        except ValueError:
            return dialogoWarninFormatError("voltaje"), 200

    if bateria:
        print("Bateria marcada")
        bateria_value = request.form.get('bateria_valor')
        intBateria = int(bateria_value)
        if bateria_value is None:
            return dialogowarningRequired("bateria"), 200
        db_methods.eliminarDatosConfig("bateria")
        db_methods.guardarDatoConfig("bateria", intBateria, True)
        try:
            float(bateria_value)
        except ValueError:
            return dialogoWarninFormatError("bateria"), 200

    if temperatura:
        print("Temperatura marcada")
        temperatura_value = request.form.get('temperatura_valor')
        intTemperatura = int(temperatura_value)
        if temperatura_value is None:
            return dialogowarningRequired("temperatura"), 200
        db_methods.eliminarDatosConfig("temperatura")
        db_methods.guardarDatoConfig("temperatura", intTemperatura, True)
        try:
            float(temperatura_value)
        except ValueError:
            return dialogoWarninFormatError("temperatura"), 200

    if autonomia:
        print("Autonomia marcada")
        autonomia_value = request.form.get('autonomia_valor')
        intAutonomia = int(autonomia_value)
        if autonomia_value is None:
            return dialogowarningRequired("autonomia"), 200
        db_methods.eliminarDatosConfig("autonomia")
        db_methods.guardarDatoConfig("autonomia", intAutonomia, True)
        try:
            float(autonomia_value)
        except ValueError:
            return dialogoWarninFormatError("autonomia"), 200

    if kilometraje:
        print("Kilometraje marcado")
        kilometraje_value = request.form.get('kilometraje_valor')
        intKilometraje = int(kilometraje_value)
        if kilometraje_value is None:
            return dialogowarningRequired("kilometraje"), 200
        db_methods.eliminarDatosConfig("kilometraje")
        db_methods.guardarDatoConfig("kilometraje", intKilometraje, True)
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

@api_cb.route('/api/get_config_bot/<name>', methods=['GET'])
def get_config_bot(name):
    data = db_methods.obtenerDatoConfig(name)
    return jsonify(data)
