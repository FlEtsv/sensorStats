import sqlite3
from auxiliar.manipulacionDatos.codigo import generarCodigoAleatorio

class Database:
    def create_database_users(self):
        conn, cursor = self.conectarBaseDatos()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                token TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                verified BOOLEAN NOT NULL,
                codigo_verificacion TEXT NOT NULL,
                chat_id INTEGER
                
            )
        ''')
        conn.commit()
        conn.close()

    def create_database_config(self):
        conn, cursor = self.conectarBaseDatos()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_variable TEXT NOT NULL,
                value_limit INTEGER NOT NULL,
                is_active BOOLEAN NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def conectarBaseDatos(self):
        conn = sqlite3.connect('data/historialDatos/telegram_bot.db')
        cursor = conn.cursor()
        return conn, cursor

class DatabaseService:
    def __init__(self):
        self.database = Database()

    def create_database_users(self):
        self.database.create_database_users()

    def create_database_config(self):
        self.database.create_database_config()

    def introducir_datos_config_defecto(self):
        conn, cursor = self.database.conectarBaseDatos()
        cursor.execute('''
            INSERT INTO config (name_variable, value_limit, is_active) VALUES (?, ?, ?)
        ''', ('voltaje', 0, False))
        cursor.execute('''
            INSERT INTO config (name_variable, value_limit, is_active) VALUES (?, ?, ?)
        ''', ('bateria', 0, False))
        cursor.execute('''
            INSERT INTO config (name_variable, value_limit, is_active) VALUES (?, ?, ?)
        ''', ('temperatura', 0, False))
        cursor.execute('''
            INSERT INTO config (name_variable, value_limit, is_active) VALUES (?, ?, ?)
        ''', ('autonomia', 0, False))
        cursor.execute('''
            INSERT INTO config (name_variable, value_limit, is_active) VALUES (?, ?, ?)
        ''', ('kilometraje', 0, False))
        conn.commit()
        conn.close()

    def obtener_dato_config(self, name):
        try:
            conn, cursor = self.database.conectarBaseDatos()
            cursor.execute('SELECT id, name_variable, value_limit, is_active FROM config WHERE name_variable = ?',
                           (name,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    'id': row[0],
                    'name_variable': row[1],
                    'value_limit': row[2],
                    'is_active': row[3]
                }
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def guardar_dato_config(self, name, value_limit, is_active):
        conn, cursor = self.database.conectarBaseDatos()
        cursor.execute('''
            UPDATE config SET value_limit = ?, is_active = ? WHERE name_variable = ?
        ''', (value_limit, is_active, name))
        conn.commit()
        conn.close()
    def eliminar_datos_config(self, name):
        conn, cursor = self.database.conectarBaseDatos()
        cursor.execute('DELETE FROM config WHERE name_variable = ?', (name,))
        conn.commit()
        conn.close()
    def guardar_datos_web(self, name, token, phone_number):
        codigo_verificacion = generarCodigoAleatorio()
        conn, cursor = self.database.conectarBaseDatos()
        cursor.execute('''
            INSERT INTO users (name, token, phone_number, verified, codigo_verificacion) VALUES (?, ?, ?, ?, ?)
        ''', (name, token, phone_number, False, codigo_verificacion))
        conn.commit()
        conn.close()
        return codigo_verificacion

    def verificar_conexion_base_datos(self):
        conn, cursor = self.database.conectarBaseDatos()
        if conn is None:
            return False
        return True

    def verificar_token(self):
        conn, cursor = self.database.conectarBaseDatos()
        cursor.execute('SELECT 1 FROM users WHERE token IS NOT NULL OR phone_number IS NOT NULL OR name IS NOT NULL LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        return bool(row)

    def eliminar_datos(self):
        print("Connecting to database")
        conn, cursor = self.database.conectarBaseDatos()
        print("Connected to database")
        try:
            print("Executing DELETE FROM users")
            cursor.execute('DELETE FROM users')
            conn.commit()
            print("Data deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while deleting data: {e}")
        finally:
            conn.close()
            print("Database connection closed")