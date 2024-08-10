from flask import Blueprint, request, redirect, url_for, render_template, make_response
from auxiliar.manipulacionDatos.BD.repository import MetodosDatabase

db_methods = MetodosDatabase()
bot_v = Blueprint('bot_v', __name__)

def no_cache(view):
    def no_cache_wrapper(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    no_cache_wrapper.__name__ = f"{view.__name__}_no_cache"
    return no_cache_wrapper

@bot_v.route('/bot/bot', methods=['GET', 'POST'])
@no_cache
def bot():
    if request.method == 'POST':
        name = request.form['name']
        token = request.form['token']
        phone_number = request.form['Numero']
        try:
            db_methods.create_database_users()
            verification_code = db_methods.guardarDatosWeb(name, token, phone_number)
            return redirect(url_for('bot_v.success_no_cache', codigoVerificacion=verification_code))
        except Exception as e:
            print(f"Error in bot route: {e}")
            return redirect(url_for('index_get'))

@bot_v.route('/success/<codigoVerificacion>')
@no_cache
def success(codigoVerificacion):
    return render_template('success.html', codigoVerificacion=codigoVerificacion)

@bot_v.route('/configuracionBot', methods=['GET'])
@no_cache
def configuracionBot():
    try:
        db_methods.create_database_users()
        token_verified = db_methods.verificarToken()
        bot_registered = token_verified
        return render_template('BotDisplay.html', botEstaRegistrado=bot_registered)
    except Exception as e:
        print(f"Error in configuracionBot route: {e}")
        return redirect(url_for('index_get'))

@bot_v.route('/bot/eliminar', methods=['GET'])
@no_cache
def eliminarBots():
    print("Entering eliminarBots route")
    try:
        db_methods.eliminarDatos()
        print("Datos eliminados correctamente")
    except Exception as e:
        print(f"Error al eliminar los datos: {e}")
    finally:
        return redirect(url_for('index_get'))