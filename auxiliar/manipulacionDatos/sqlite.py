import sqlite3

from auxiliar.manipulacionDatos.codigo import generarCodigoAleatorio


def create_database():
    conn, cursor = conectarBaseDatos()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            token TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            verified BOOLEAN NOT NULL,
            codigo_verificacion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardarDatosWeb(name, token, phone_number):
    codigoVerificacion = generarCodigoAleatorio()
    conn, cursor = conectarBaseDatos()
    cursor.execute('''
        INSERT INTO users (name, token, phone_number, verified, codigo_verificacion) VALUES (?, ?, ?, ?, ?)
    ''', (name, token, phone_number, False, codigoVerificacion))
    conn.commit()
    conn.close()
    return codigoVerificacion

def conectarBaseDatos():
    conn = sqlite3.connect('data/historialDatos/telegram_bot.db')
    cursor = conn.cursor()
    return conn, cursor

def verificarConexionBaseDatos():
    conn, cursor = conectarBaseDatos()
    if conn is None:
        return False
    return True