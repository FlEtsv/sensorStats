
from auxiliar.manipulacionDatos.BD.servicesBD.sqlite import DatabaseService, Database


class MetodosDatabase:
    def __init__(self):
        self.service = Database()
        self.dataService = DatabaseService()

    def create_database_users(self):
        try:
            print("Creating database users in MetodosDatabase")
            self.service.create_database_users()
            print("Database users created successfully in MetodosDatabase")
        except Exception as e:
            print(f"Error in create_database_users: {e}")

    def create_database_config(self):
        try:
            print("Creating database config in MetodosDatabase")
            self.service.create_database_config()
            print("Database config created successfully in MetodosDatabase")
        except Exception as e:
            print(f"Error in create_database_config: {e}")

    def introducirDatosConfigDefecto(self):
        try:
            print("Introducing default config data in MetodosDatabase")
            self.dataService.introducir_datos_config_defecto()
            print("Default config data introduced successfully in MetodosDatabase")
        except Exception as e:
            print(f"Error in introducirDatosConfigDefecto: {e}")

    def obtenerDatoConfig(self, name):
        try:
            print(f"Obtaining config data for {name} in MetodosDatabase")
            result = self.dataService.obtener_dato_config(name)
            print(f"Config data obtained for {name} in MetodosDatabase: {result}")
            return result
        except Exception as e:
            print(f"Error in obtenerDatoConfig: {e}")
            return None

    def guardarDatoConfig(self, name, value_limit, is_active):
        try:
            print(f"Saving config data for {name} in MetodosDatabase")
            self.dataService.guardar_dato_config(name, value_limit, is_active)
            print("Config data saved successfully in MetodosDatabase")
        except Exception as e:
            print(f"Error in guardarDatoConfig: {e}")

    def guardarDatosWeb(self, name, token, phone_number):
        try:
            print(f"Saving web data for {name} in MetodosDatabase")
            result = self.dataService.guardar_datos_web(name, token, phone_number)
            print(f"Web data saved for {name} in MetodosDatabase: {result}")
            return result
        except Exception as e:
            print(f"Error in guardarDatosWeb: {e}")
            return None

    def verificarConexionBaseDatos(self):
        try:
            print("Verifying database connection in MetodosDatabase")
            result = self.dataService.verificar_conexion_base_datos()
            print(f"Database connection verified in MetodosDatabase: {result}")
            return result
        except Exception as e:
            print(f"Error in verificarConexionBaseDatos: {e}")
            return False

    def verificarToken(self):
        try:
            print("Verifying token in MetodosDatabase")
            result = self.dataService.verificar_token()
            print(f"Token verified in MetodosDatabase: {result}")
            return result
        except Exception as e:
            print(f"Error in verificarToken: {e}")
            return False

    def eliminarDatos(self):
        try:
            print("Deleting data in MetodosDatabase")
            self.dataService.eliminar_datos()
            print("Data deleted successfully in MetodosDatabase")
        except Exception as e:
            print(f"Error in eliminarDatos: {e}")