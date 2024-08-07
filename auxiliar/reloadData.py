import logging
import threading
import time

from apscheduler.triggers import interval

from auxiliar import utilidades, sesion
from auxiliar.data import get_data
from auxiliar.indexBack.indexBack import extract_vehicle_data

def recargarPaginatimer():
    logging.debug("Starting recargarPaginatimer")
    api_url = utilidades.construirAPI(sesion.sesion.get_instance().get_ip_port(), sesion.sesion.get_instance().get_vin())
    logging.debug(f"Constructed API URL: {api_url}")
    data = get_data(api_url)
    if data:
        logging.debug("Data fetched successfully")
        extract_vehicle_data(data)
        logging.info("Datos del vehículo cargados con éxito.")
    else:
        logging.debug("Failed to fetch data")

def tarea_programada():
    logging.debug("Starting tarea_programada")
    recargarPaginatimer()
    print("Tarea ejecutada")
    logging.debug("Finished tarea_programada")

def run_periodic_task(interval):
    logging.debug("Entering run_periodic_task")
    while True:
        logging.debug("About to call tarea_programada")
        tarea_programada()
        logging.debug("Called tarea_programada2, now sleeping")
        time.sleep(interval)

def initReload():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("Starting the application")
    interval =  10800 # Interval in seconds
    # Iniciar la tarea periódica en un hilo separado
    logging.debug("Starting the periodic task thread")
    thread = threading.Thread(target=run_periodic_task(interval))
    thread.daemon = True  # Ensure the thread will close when the main program exits
    thread.start()

    logging.debug("Timer started")