def evaluar(value, data_type):
    if data_type == 'battery_voltage':
        if 330 <= value <= 360:
            return 'amarillo'
        elif value < 330:
            return 'rojo'
        else:
            return 'verde'
    elif data_type == 'autonomy':
        if value < 100:
            return 'rojo'
        elif 101 <= value <= 200:
            return 'amarillo'
        else:
            return 'verde'
    elif data_type == 'energy':
        if 35 < value < 65:
            return 'amarillo'
        elif value <= 35:
            return 'rojo'
        else:
            return 'verde'
    elif data_type == 'air_temp':
        if 34.5 > value > 30:
            return 'amarillo'
        elif 0 <= value <= 30:
            return 'verde'
        else:
            return 'rojo'
    elif data_type == 'level':
        if value < 30:
            return 'rojo'
        elif 31 <= value <= 60:
            return 'amarillo'
        else:
            return 'verde'
    else:
        return 'blanco'

def evaluarIndex(value, data_type):
    if data_type == 'battery_voltage':
        if (82.5<= value <= 90):
            return 'chart-card-amarillo'
        elif value < 82.5:
            return 'chart-card-rojo'
        else:
            return 'chart-card-verde'
    elif data_type == 'autonomy':
        if value < 100:
            return 'chart-card-rojo'
        elif 100 <= value <= 200:
            return 'chart-card-amarillo'
        else:
            return 'chart-card-verde'
    elif data_type == 'air_temp':
        if 30 < value < 34.5:
            return 'chart-card-amarillo'
        elif 0 <= value <= 30:
            return 'chart-card-verde'
        else:
            return 'chart-card-rojo'
    elif data_type == 'level':
        if value < 30:
            return 'chart-card-rojo'
        elif 30 <= value <= 60:
            return 'chart-card-amarillo'
        else:
            return 'chart-card-verde'
    elif data_type == "luminosity_day":
        if value == False:
            return 'chart-card-rojo'
        else:
            return 'chart-card-verde'
    elif data_type == "preconditioning_status":
        if value == "Disabled":
            return 'chart-card-rojo'
        else:
            return 'chart-card-verde'
    elif data_type == "charging_status":
        if value == "Disconnected":
            return 'chart-card-rojo'
        else:
            return 'chart-card-verde'
    elif data_type == "charging_mode":
        if value == "No":
            return 'chart-card-rojo'
        elif value == "Slow":
            return 'chart-card-amarillo'
    else:
        return 'chart-card'