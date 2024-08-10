import logging
import threading
import time

from apscheduler.triggers import interval

from auxiliar import utilidades, sesion
from auxiliar.data import get_data
from auxiliar.indexBack.indexBack import extract_vehicle_data


class ReloadData:
    def __init__(self):
        self.sesion_instance = sesion.sesion.get_instance()
    def recargarPaginatimer(self):

        logging.debug("Starting recargarPaginatimer")
        api_url = utilidades.construirAPI( self.sesion_instance.get_ip_port(), self.sesion_instance.get_vin())
        logging.debug(f"Constructed API URL: {api_url}")
        logging.info(api_url)
        data = get_data(api_url)
        if data:
            logging.debug("Data fetched successfully")
            extract_vehicle_data(data)
            logging.info("Datos del vehículo cargados con éxito.")
        else:
            logging.debug("Failed to fetch data")

    def tarea_programada(self):
        logging.debug("Starting tarea_programada")
        self.recargarPaginatimer()
        print("Tarea ejecutada")
        logging.debug("Finished tarea_programada")

    def run_periodic_task(self, interval):
        logging.debug("Entering run_periodic_task")
        while not self.sesion_instance.get_ip_port() or not self.sesion_instance.get_vin():
            logging.debug("Waiting for IP and VIN to be set")
            time.sleep(60)
        while True:
            logging.debug("About to call tarea_programada")
            self.tarea_programada()
            logging.debug("Called tarea_programada, now sleeping")
            time.sleep(interval)

    def initReload(self):
        #metodo que espera que se inicie la aplicacion para iniciar el hilo

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.debug("Starting the application")
        interval = 10800  # Interval in seconds
        # Iniciar la tarea periódica en un hilo separado
        logging.debug("Starting the periodic task thread")
        thread = threading.Thread(target=self.run_periodic_task, args=(interval,))
        thread.daemon = True  # Ensure the thread will close when the main program exits
        thread.start()

        logging.debug("Timer started")