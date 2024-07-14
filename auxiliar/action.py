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
    else:
        return 'blanco'