from flask import jsonify, Blueprint

from auxiliar.data import get_data_boolean
from auxiliar.manipulacionDatos.BD.repository import MetodosDatabase
from auxiliar.sesion import sesion
from auxiliar.utilidades import construirAPI
db_methods = MetodosDatabase()

api_cn = Blueprint('api_cn', __name__)

@api_cn.route('/api/alive', methods=['GET'])
def alive():
    try:
        if not chequeoSalud():
            return jsonify({"status": "not alive"}), 500
        return jsonify({"status": "alive"}), 200
    except Exception as e:
        return jsonify({"status": "not alive", "error": str(e)}), 500

def chequeoSalud():
    # verificamos la conexion a la api
    ip_port = sesion.get_instance().get_ip_port()
    vin = sesion.get_instance().get_vin()
    if not ip_port or not vin:
        return False
    api = get_data_boolean(construirAPI(ip_port, vin))
    if api is False:
        return False
    # verificamos la conexion a la base de datos
    if db_methods.verificarConexionBaseDatos() is False:
        return False

    return True
