import math

def get_compass(mag_data):
    """
    Restituisce l'angolo di rotta
    :param mag_data:
    :return:
    """
    return math.atan2(mag_data[1], mag_data[0])

